from datetime import timedelta
from time import sleep
import os
from pathlib import Path
from time import time
import json

from zero_sdk.exceptions import TransactionError
from zero_sdk.transaction import Transaction
from zero_sdk.network import Network
from zero_sdk.utils import generate_random_letters, create_allocation
from zero_sdk.bls import sign_payload
from zero_sdk.connection import ConnectionBase
from zero_sdk.miner_settings import miner_delegate_pool
from zero_sdk.const import (
    INTEREST_POOL_SMART_CONTRACT_ADDRESS,
    STORAGE_SMART_CONTRACT_ADDRESS,
    FAUCET_SMART_CONTRACT_ADDRESS,
    MINER_SMART_CONTRACT_ADDRESS,
    Endpoints,
    AllocationConfig,
    TransactionType,
    TransactionName,
)


class Wallet(ConnectionBase):
    def __init__(
        self,
        client_id,
        client_key,
        public_key,
        private_key,
        mnemonics,
        date_created,
        network,
        version="1.0",
    ):
        self.client_id = client_id
        self.client_key = client_key
        self.public_key = public_key
        self.private_key = private_key
        self.mnemonics = mnemonics
        self.version = version
        self.date_created = date_created
        self.network = network

    def _init_wallet(self):
        # Implement wallet init
        pass

    def _validate_wallet(method):
        """Initialize wallet
        Check the wallet is initialized before every API request
        If wallet is not initialized, create a new wallet.
        """

        def wrapper(self, *args, **kwargs):
            print(self)

            if self.client_id is not None:
                return method(self, *args, **kwargs)
            else:
                self._init_wallet()
                raise Exception(
                    "Wallet is not initialized, call 'create_wallet, init_wallet or recover_wallet' methods to configure wallet"
                )

        return wrapper

    def get_balance(self, format="default") -> int:
        """Get Wallet balance
        Return float value of tokens
        """
        endpoint = f"{Endpoints.GET_BALANCE}?client_id={self.client_id}"
        empty_return_value = {"balance": 0}
        res = self._consensus_from_workers(
            "sharders", endpoint, empty_return_value=empty_return_value
        )
        try:
            bal = res.get("balance")
            if format == "default":
                return bal
            elif format == "human":
                return "%.10f" % (bal / 10000000000)
            else:
                return bal

        except AttributeError:
            return res

    def get_pool_info(self, node_id, pool_id):
        endpoint = f"{Endpoints.GET_MINERSC_POOL_STATS}?id={node_id}&pool_id={pool_id}"
        empty_return_value = {"pools": {}}
        res = self._consensus_from_workers(
            "sharders", endpoint, empty_return_value=empty_return_value
        )
        return res

    def get_user_pool_info(self):
        endpoint = f"{Endpoints.GET_MINERSC_USER_STATS}?client_id={self.client_id}"
        empty_return_value = {"pools": {}}
        res = self._consensus_from_workers(
            "sharders", endpoint, empty_return_value=empty_return_value
        )
        try:
            return res.get("pools")
        except:
            return res

    def get_read_pool_info(self, allocation_id=None):
        url = f"{Endpoints.SC_REST_READPOOL_STATS}?client_id={self.client_id}"
        res = self._consensus_from_workers("sharders", url)

        if allocation_id:
            return self._filter_by_allocation(res, allocation_id)
        return res

    def get_write_pool_info(self, allocation_id=None):
        url = f"{Endpoints.SC_REST_WRITEPOOL_STATS}?client_id={self.client_id}"
        res = self._consensus_from_workers("sharders", url)

        if allocation_id:
            return self._filter_by_allocation(res, allocation_id)

        return res

    def list_allocations(self):
        url = f"{Endpoints.SC_REST_ALLOCATIONS}?client={self.client_id}"
        res = self._consensus_from_workers("sharders", url)
        return res

    def get_allocation_info(self, allocation_id):
        alocs = self.list_allocations()
        return self._filter_by_allocation(alocs, allocation_id, "list")

    # --------------
    # Smart Contract Methods
    # --------------

    def add_tokens(self):
        input = "give me tokens"
        return self._handle_transaction(
            sc_address=FAUCET_SMART_CONTRACT_ADDRESS,
            transaction_name=TransactionName.ADD_TOKEN,
            input=input,
            value=1,
        )

    def create_allocation(
        self,
        data_shards=AllocationConfig.DATA_SHARDS,
        parity_shards=AllocationConfig.PARITY_SHARDS,
        size=AllocationConfig.SIZE,
        lock_tokens=AllocationConfig.TOKEN_LOCK,
        preferred_blobbers=AllocationConfig.PREFERRED_BLOBBERS,
        write_price=AllocationConfig.WRITE_PRICE,
        read_price=AllocationConfig.READ_PRICE,
        max_challenge_completion_time=AllocationConfig.MAX_CHALLENGE_COMPLETION_TIME,
        expiration_date=time(),
    ):
        future_date = int(expiration_date + timedelta(days=30).total_seconds())
        input = {
            "data_shards": data_shards,
            "parity_shards": parity_shards,
            "owner_id": self.client_id,
            "owner_public_key": self.public_key,
            "size": size,
            "expiration_date": future_date,
            "read_price_range": read_price,
            "write_price_range": write_price,
            "max_challenge_completion_time": max_challenge_completion_time,
            "preferred_blobbers": preferred_blobbers,
        }

        return self._handle_transaction(
            transaction_name=TransactionName.NEW_ALLOCATION_REQUEST,
            input=input,
            value=lock_tokens,
        )

    def lock_tokens(self, amount, hours=0, minutes=0):
        if hours < 0 or minutes < 0:
            raise Exception("Invalid time")

        input = {"duration": f"{hours}h{minutes}m"}
        return self._handle_transaction(
            transaction_name=TransactionName.LOCK_TOKEN,
            input=input,
            wallet=self,
            value=amount,
            sc_address=INTEREST_POOL_SMART_CONTRACT_ADDRESS,
        )

    def create_read_pool(self):
        input = None
        return self._handle_transaction(
            transaction_name=TransactionName.STORAGESC_CREATE_READ_POOL,
            input=input,
            raise_exception=True,
        )

    def miner_lock_token(
        self,
        amount,
        id,
    ):
        """Lock tokens on miner"""
        input = {"id": id}
        return self._handle_transaction(
            transaction_name=TransactionName.MINERSC_LOCK,
            input=input,
            value=amount,
            sc_address=MINER_SMART_CONTRACT_ADDRESS,
            raise_exception=True,
        )

    def miner_unlock_token(self, node_id, pool_id):
        input = {"id": node_id, "pool_id": pool_id}
        return self._handle_transaction(
            transaction_name=TransactionName.MINERSC_UNLOCK,
            input=input,
            sc_address=MINER_SMART_CONTRACT_ADDRESS,
            raise_exception=True,
        )

    def update_miner_settings(
        self,
        miner_id="",
        miner_url="",
        delegate_wallet="",
        service_charge=0,
        num_delegates=0,
        min_stake=0,
        max_stake=0,
        block_reward=None,
        service_charge_stat=None,
        users_fee=None,
        block_sharders_fee=None,
        sharder_rewards=None,
        pending_pools=[miner_delegate_pool],
        active_pools=[miner_delegate_pool],
        deleting_pools=[miner_delegate_pool],
    ):

        miner_stat = {
            "block_reward,omitempty": block_reward,
            "service_charge,omitempty": service_charge_stat,
            "users_fee,omitempty": users_fee,
            "block_sharders_fee,omitempty": block_sharders_fee,
            "sharder_rewards,omitempty": sharder_rewards,
        }

        simple_miner_info = {
            "id": miner_id,
            "url": miner_url,
            "delegate_wallet": delegate_wallet,
            "service_charge": service_charge,
            "number_of_delegates": num_delegates,
            "min_stake": min_stake,
            "max_stake": max_stake,
            "stat": miner_stat,
        }

        input = {
            "simple_miner": simple_miner_info,
            "pending": pending_pools,
            "active": active_pools,
            "deleting_pools": deleting_pools,
        }

    # --------------
    # Private Methods
    # --------------

    def _handle_transaction(
        self,
        transaction_name,
        input,
        transaction_type=TransactionType.SMART_CONTRACT,
        value=0,
        sc_address=STORAGE_SMART_CONTRACT_ADDRESS,
        raise_exception=False,
    ):
        transaction = Transaction.create_transaction(
            transaction_name=transaction_name,
            transaction_type=transaction_type,
            input=input,
            wallet=self,
            value=value,
            sc_address=sc_address,
        )
        transaction.execute()
        data = transaction.validate(raise_exception)

        return data

    def _filter_by_allocation(self, res, allocation_id, format="dict"):
        pool_info = []
        if format == "list":
            for aloc in res:
                if aloc["id"] == allocation_id:
                    return aloc

        elif allocation_id and res["pools"]:
            pools = res["pools"]
            for pool in pools:
                if pool["allocation_id"] == allocation_id:
                    pool_info.append(pool)

            if len(pool_info) == 0:
                return []
            else:
                return pool_info

    # --------------------
    # Versing pool methods
    # --------------------

    def get_vesting_pool_config(self):
        endpoint = Endpoints.VP_GET_CONFIG
        res = self._consensus_from_workers("sharders", endpoint)
        return res

    def sign(self, payload):
        return sign_payload(self.private_key, payload)

    def save(self, wallet_name=None):
        if not wallet_name:
            wallet_name = generate_random_letters()

        data = {
            "client_id": self.client_id,
            "client_key": self.public_key,
            "keys": [{"public_key": self.public_key, "private_key": self.private_key}],
            "mnemonics": self.mnemonics,
            "version": self.version,
            "date_created": self.date_created,
        }

        with open(
            os.path.join(Path.home(), f".zcn/test_wallets/wallet_{wallet_name}.json"),
            "w",
        ) as f:
            f.write(json.dumps(data, indent=4))

    @staticmethod
    def from_object(config: dict, network: Network):
        """Returns fully configured instance of wallet
        :param config: Wallet config object from json.loads function
        :param network: Instance of configured network
        """
        return Wallet(
            config.get("client_id"),
            config.get("client_key"),
            config.get("keys")[0]["public_key"],
            config.get("keys")[0]["private_key"],
            config.get("mnemonics"),
            config.get("date_created"),
            network,
            config.get("version"),
        )

    def __repr__(self):
        return f"Wallet(config, network)"

    def __str__(self):
        return f"client_id: {self.client_id} \nnetwork_url: {self.network.hostname}"

    # -----------------
    # TODO: Fix methods
    # All below methods need confirmation
    # -----------------

    def blobber_lock_token(self, transaction_value, blobber_id):
        """Lock tokens on blobber"""
        payload = json.dumps(
            {"name": "stake_pool_lock", "input": {"blobber_id": blobber_id}}
        )
        res = self._execute_smart_contract(
            to_client_id=STORAGE_SMART_CONTRACT_ADDRESS,
            transaction_value=transaction_value,
            payload=payload,
        )
        return res

    def blobber_unlock_token(self, pool_id, blobber_id):
        """Unlock tokens from pool id and blobber"""
        payload = json.dumps(
            {
                "name": "stake_pool_unlock",
                "input": {"pool_id": pool_id, "blobber_id": blobber_id},
            }
        )
        res = self._execute_smart_contract(
            to_client_id=STORAGE_SMART_CONTRACT_ADDRESS,
            payload=payload,
        )
        return res

    def get_locked_tokens(self):
        endpoint = f"{Endpoints.GET_LOCKED_TOKENS}?client_id={self.client_id}"
        empty_return_value = {
            "message": "Failed to get locked tokens.",
            "code": "resource_not_found",
            "error": "resource_not_found: can't find user node",
        }
        res = self._consensus_from_workers(
            "sharders", endpoint, empty_return_value=empty_return_value
        )
        return res

    def get_lock_config(self):
        endpoint = Endpoints.GET_LOCK_CONFIG
        res = self._consensus_from_workers("sharders", endpoint)
        return res

    def allocation_min_lock(
        self,
        data_shards=AllocationConfig.DATA_SHARDS,
        parity_shards=AllocationConfig.PARITY_SHARDS,
        size=AllocationConfig.SIZE,
        preferred_blobbers=AllocationConfig.PREFERRED_BLOBBERS,
        write_price=AllocationConfig.WRITE_PRICE,
        read_price=AllocationConfig.READ_PRICE,
        max_challenge_completion_time=AllocationConfig.MAX_CHALLENGE_COMPLETION_TIME,
        expiration_date=time(),
    ):
        future = int(expiration_date + timedelta(days=30).total_seconds())

        payload = json.dumps(
            {
                "allocation_data": {
                    "data_shards": data_shards,
                    "parity_shards": parity_shards,
                    "owner_id": self.client_id,
                    "owner_public_key": self.public_key,
                    "size": size,
                    "expiration_date": future,
                    "read_price_range": read_price,
                    "write_price_range": write_price,
                    "max_challenge_completion_time": max_challenge_completion_time,
                    "preferred_blobbers": preferred_blobbers,
                },
            }
        )

        res = self._consensus_from_workers(
            "sharders", endpoint=Endpoints.SC_REST_ALLOCATION_MIN_LOCK, data=payload
        )
        return res

    def update_allocation(
        self,
        allocation_id,
        tokens=1,
        extend_expiration_hours=720,
        size=2147483652,
    ):
        future = int(time() + timedelta(hours=extend_expiration_hours).total_seconds())

        payload = json.dumps(
            {
                "name": "update_allocation_request",
                "input": {
                    "owner_id": self.client_id,
                    "id": allocation_id,
                    "size": size,
                    "expiration_date": future,
                },
            }
        )
        res = self._execute_smart_contract(payload, transaction_value=tokens)

        return res
