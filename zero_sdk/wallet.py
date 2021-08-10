from datetime import timedelta
import os
from pathlib import Path
from time import time
import json

from zero_sdk.const import (
    AllocationConfig,
    Endpoints,
    FAUCET_SMART_CONTRACT_ADDRESS,
    MINER_SMART_CONTRACT_ADDRESS,
    TransactionType,
    STORAGE_SMART_CONTRACT_ADDRESS,
)
from zero_sdk.network import Network
from zero_sdk.utils import hash_string, generate_random_letters, create_allocation
from zero_sdk.bls import sign_payload
from zero_sdk.connection_base import ConnectionBase


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

    def _execute_smart_contract(self, payload, to_client_id=None, transaction_value=0):
        if not to_client_id:
            to_client_id = STORAGE_SMART_CONTRACT_ADDRESS
        return self._submit_transaction(
            to_client_id, transaction_value, payload, TransactionType.SMART_CONTRACT
        )

    def _execute_faucet_smart_contract(
        self, method_name="pour", input="pour_tokens", transaction_value=10000000000
    ):
        payload = json.dumps({"name": method_name, "input": input})

        return self._execute_smart_contract(
            to_client_id=FAUCET_SMART_CONTRACT_ADDRESS,
            transaction_value=transaction_value,
            payload=payload,
        )

    def _submit_transaction(self, to_client_id, value, payload, transaction_type):
        hash_payload = hash_string(payload)
        ts = int(time())

        hashdata = f"{ts}:{self.client_id}:{to_client_id}:{value}:{hash_payload}"

        hash = hash_string(hashdata)
        signature = self.sign(hash)

        data = json.dumps(
            {
                "client_id": self.client_id,
                "public_key": self.public_key,
                "transaction_value": value,
                "transaction_data": payload,
                "transaction_type": transaction_type,
                "creation_date": ts,
                "to_client_id": to_client_id,
                "hash": hash,
                "transaction_fee": 0,
                "signature": signature,
                "version": "1.0",
            }
        )
        headers = {"Content-Type": "application/json"}
        res = self._consensus_from_workers(
            "miners",
            endpoint=Endpoints.PUT_TRANSACTION,
            method="POST",
            data=data,
            headers=headers,
        )
        return res

    def get_balance(self) -> int:
        """Get Wallet balance
        Return float value of tokens
        """
        endpoint = f"{Endpoints.GET_BALANCE}?client_id={self.client_id}"
        empty_return_value = {"balance": 0}
        data = self._consensus_from_workers(
            "sharders", endpoint, empty_return_value=empty_return_value
        )

        return data

    def get_user_pools(self):
        endpoint = f"{Endpoints.GET_USER_POOLS}?client_id={self.client_id}"
        empty_return_value = {"pools": {}}
        res = self._consensus_from_workers(
            "sharders", endpoint, empty_return_value=empty_return_value
        )
        return res

    def add_tokens(self):
        return self._execute_faucet_smart_contract()

    def get_read_pool_info(self):
        url = f"{Endpoints.SC_REST_READPOOL_STATS}?client_id={self.client_id}"
        res = self._consensus_from_workers("sharders", url)
        return res

    def get_write_pool_info(self):
        url = f"{Endpoints.SC_REST_WRITEPOOL_STATS}?client_id={self.client_id}"
        res = self._consensus_from_workers("sharders", url)
        return res

    def list_allocations(self):
        url = f"{Endpoints.SC_REST_ALLOCATIONS}?client={self.client_id}"
        res = self._consensus_from_workers("sharders", url)
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

    def miner_unlock_token(self, pool_id, id, type):
        """Unlock tokens from miner"""
        payload = json.dumps(
            {
                "name": "deleteFromDelegatePool",
                "input": {"pool_id": pool_id, "id": id, "type": type},
            }
        )
        res = self._execute_smart_contract(
            to_client_id=MINER_SMART_CONTRACT_ADDRESS,
            payload=payload,
        )
        return res

    def miner_lock_token(self, transaction_value, id, type):
        """Lock tokens on miner"""
        payload = json.dumps(
            {"name": "addToDelegatePool", "input": {"id": id, "type": type}}
        )
        res = self._execute_smart_contract(
            to_client_id=MINER_SMART_CONTRACT_ADDRESS,
            transaction_value=transaction_value,
            payload=payload,
        )
        return res

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
        empty_return_value = {"locked_tokens": []}
        res = self._consensus_from_workers(
            "sharders", endpoint, empty_return_value=empty_return_value
        )
        return res

    def create_read_pool(self):
        payload = json.dumps({"name": "new_read_pool", "input": None})
        res = self._execute_smart_contract(payload)
        return res

    def allocate_storage(
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
        future = int(expiration_date + timedelta(days=30).total_seconds())
        # future = 1628610719

        payload = json.dumps(
            {
                "name": "new_allocation_request",
                "input": {
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

        print("Request Payload", json.dumps(payload, indent=4))

        res = self._execute_smart_contract(payload, transaction_value=lock_tokens)
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
        expiration_date=2592000,
        size=2147483648,
    ):
        payload = json.dumps(
            {
                "name": "update_allocation_request",
                "input": {
                    "owner_id": self.client_id,
                    "id": allocation_id,
                    "size": size,
                    "expiration_date": expiration_date,
                },
            }
        )
        res = self._execute_smart_contract(payload, transaction_value=tokens)

        return res
