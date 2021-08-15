from datetime import timedelta
import os
from pathlib import Path
from time import time
import json
from zerochain.allocation import Allocation

from zerochain.transaction import Transaction
from zerochain.network import Network
from zerochain.utils import generate_random_letters, get_duration_nanoseconds
from zerochain.bls import sign_payload
from zerochain.connection import ConnectionBase
from zerochain.miner_settings import miner_delegate_pool
from zerochain.wallet_methods.vesting import VestingMethods
from zerochain.wallet_methods.allocation import AllocationMethods
from zerochain.wallet_methods.blobber import BlobberMethods
from zerochain.const import (
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
        mnemonic,
        date_created,
        network,
        version="1.0",
    ):
        self.client_id = client_id
        self.client_key = client_key
        self.public_key = public_key
        self.private_key = private_key
        self.mnemonic = mnemonic
        self.version = version
        self.date_created = date_created
        self.network = network

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

    def list_lock_token(self):
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

    def list_miners(self):
        return self.network.list_miners()

    def list_sharders(self):
        return self.network.list_sharders()

    def get_stake_pool_info(self, node_id, pool_id):
        endpoint = f"{Endpoints.GET_MINERSC_POOL_STATS}?id={node_id}&pool_id={pool_id}"
        empty_return_value = {"pools": {}}
        res = self._consensus_from_workers(
            "sharders", endpoint, empty_return_value=empty_return_value
        )
        return res

    def list_stake_pool_info(self):
        endpoint = f"{Endpoints.GET_MINERSC_USER_STATS}?client_id={self.client_id}"
        empty_return_value = {"pools": {}}
        res = self._consensus_from_workers(
            "sharders", endpoint, empty_return_value=empty_return_value
        )
        try:
            return res.get("pools")
        except:
            return res

    def list_read_pool_info(self, allocation_id=None):
        url = f"{Endpoints.SC_REST_READPOOL_STATS}?client_id={self.client_id}"
        res = self._consensus_from_workers("sharders", url)

        if allocation_id:
            return self._filter_by_allocation_id(res, allocation_id)

        return self._return_pools(res)

    def list_write_pool_info(self, allocation_id=None):
        url = f"{Endpoints.SC_REST_WRITEPOOL_STATS}?client_id={self.client_id}"
        res = self._consensus_from_workers("sharders", url)

        if allocation_id:
            return self._filter_by_allocation_id(res, allocation_id)

        return self._return_pools(res)

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

    def lock_token(self, amount, hours=0, minutes=0):
        if hours < 0 or minutes < 0:
            raise Exception("Invalid time")

        input = {"duration": f"{hours}h{minutes}m"}
        return self._handle_transaction(
            transaction_name=TransactionName.LOCK_TOKEN,
            input=input,
            value=amount,
            sc_address=INTEREST_POOL_SMART_CONTRACT_ADDRESS,
        )

    def unlock_token(self, pool_id):
        input = {"pool_id": pool_id}
        return self._handle_transaction(
            transaction_name=TransactionName.UNLOCK_TOKEN,
            input=input,
            sc_address=INTEREST_POOL_SMART_CONTRACT_ADDRESS,
        )

    def create_read_pool(self):
        input = None
        return self._handle_transaction(
            transaction_name=TransactionName.STORAGESC_CREATE_READ_POOL,
            input=input,
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
        )

    def miner_unlock_token(self, node_id, pool_id):
        input = {"id": node_id, "pool_id": pool_id}
        return self._handle_transaction(
            transaction_name=TransactionName.MINERSC_UNLOCK,
            input=input,
            sc_address=MINER_SMART_CONTRACT_ADDRESS,
        )

    def send_token(self, to_client_id, amount, description=""):
        input = description

        return self._handle_transaction(
            transaction_type=TransactionType.SEND,
            input=input,
            value=amount,
            sc_address=to_client_id,
        )

    # --------------------
    # Vesting Pool methods
    # --------------------

    def get_vesting_pool_config(self):
        return VestingMethods.get_vesting_pool_config(self)

    def get_vesting_pool_info(self, pool_id):
        return VestingMethods.get_vesting_pool_config(self, pool_id)

    def list_vesting_pool_info(self):
        return VestingMethods.list_vesting_pool_info(self)

    def vesting_pool_create(
        self,
        destinations,
        hours=0,
        minutes=0,
        days=0,
        description="",
        start_time=int(time()),
    ):
        return VestingMethods.vesting_pool_create(
            self, destinations, hours, minutes, days, description, start_time
        )

    def vesting_pool_delete(self, pool_id):
        return VestingMethods.vesting_pool_delete(self, pool_id)

    def vesting_pool_unlock(self, pool_id):
        return VestingMethods.vesting_pool_unlock(self, pool_id)

    def vesting_pool_trigger(self, pool_id):
        input = {"pool_id": pool_id}
        return VestingMethods.vesting_pool_trigger(self, pool_id)

    def vesting_pool_stop(self, miner_id, pool_id):
        return VestingMethods.vesting_pool_stop(self, miner_id, pool_id)

    # --------------------
    # Allocation methods
    # --------------------

    def get_sc_config(self):
        """Get storage contract config"""
        return AllocationMethods.get_sc_config(self)

    def read_pool_lock(
        self,
        amount,
        allocation_id,
        days=0,
        hours=0,
        minutes=0,
        seconds=0,
        blobber_id=None,
    ):
        return AllocationMethods.read_pool_lock(
            self, amount, allocation_id, days, hours, minutes, seconds, blobber_id
        )

    def list_read_pool_by_allocation_id(self, allocation_id):
        return AllocationMethods.list_read_pool_by_allocation_id(self, allocation_id)

    def read_pool_unlock(self, pool_id):
        return AllocationMethods.read_pool_unlock(self, pool_id)

    def list_allocations(self):
        return AllocationMethods.list_allocations(self)

    def get_allocation_info(self, allocation_id):
        return AllocationMethods.get_allocation_info(self, allocation_id)

    def get_allocation(self, allocation_id) -> Allocation:
        """Returns an instance of an allocation"""
        return AllocationMethods.get_allocation(self, allocation_id)

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
        return AllocationMethods.create_allocation(
            self,
            data_shards,
            parity_shards,
            size,
            lock_tokens,
            preferred_blobbers,
            write_price,
            read_price,
            max_challenge_completion_time,
            expiration_date,
        )

    # --------------------
    # Blobber methods
    # --------------------

    def get_blobber_info(self, blobber_id):
        """Get info for given blobber ID"""
        return BlobberMethods.get_blobber_info(self, blobber_id)

    def get_blobber_stats(self, blobber_url):
        """Get stats for given blobber url"""
        return BlobberMethods.get_blobber_info(self, blobber_url)

    def list_blobbers(self):
        """Get stats of each blobber used by the allocation, detailed
        information of allocation size and write markers per blobber"""
        return BlobberMethods.list_blobbers(self)

    def list_blobbers_by_allocation_id(self, allocation_id):
        """Get stats of each blobber used by the allocation, detailed
        information of allocation size and write markers per blobber"""
        return BlobberMethods.get_blobber_info(self, allocation_id)

    # def update_blobber_settings(self, blobber_id, )

    # --------------------
    # Utility methods
    # --------------------

    def sign(self, payload):
        return sign_payload(self.private_key, payload)

    def save(self, wallet_name=None):
        if not wallet_name:
            wallet_name = generate_random_letters()

        data = {
            "client_id": self.client_id,
            "client_key": self.public_key,
            "keys": [{"public_key": self.public_key, "private_key": self.private_key}],
            "mnemonic": self.mnemonic,
            "version": self.version,
            "date_created": self.date_created,
        }

        with open(
            os.path.join(Path.home(), f".zcn/test_wallets/wallet_{wallet_name}.json"),
            "w",
        ) as f:
            f.write(json.dumps(data, indent=4))

    # --------------
    # Private Methods
    # --------------

    def _return_pools(self, res):
        try:
            return res.get("pools")
        except:
            return res

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

    def _handle_transaction(
        self,
        input,
        transaction_name=None,
        transaction_type=TransactionType.SMART_CONTRACT,
        value=0,
        sc_address=STORAGE_SMART_CONTRACT_ADDRESS,
        raise_exception=False,
    ):
        transaction = Transaction(
            transaction_name=transaction_name,
            transaction_type=transaction_type,
            input=input,
            wallet=self,
            value=value,
            sc_address=sc_address,
            raise_exception=raise_exception,
        )
        transaction.execute()
        data = transaction.validate()

        return data

    def _filter_by_allocation_id(self, res, allocation_id, format="dict"):
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
            "block_reward": block_reward,
            "service_charge": service_charge_stat,
            "users_fee": users_fee,
            "block_sharders_fee": block_sharders_fee,
            "sharder_rewards": sharder_rewards,
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

        return self._handle_transaction(
            transaction_name=TransactionName.MINERSC_SETTINGS,
            input=input,
            sc_address=MINER_SMART_CONTRACT_ADDRESS,
        )

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
