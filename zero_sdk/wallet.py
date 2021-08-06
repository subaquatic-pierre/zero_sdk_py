from datetime import date, timedelta
import requests
from time import time
import json

from zero_sdk.const import (
    AllocationConfig,
    Endpoints,
    TransactionType,
    STORAGE_SMART_CONTRACT_ADDRESS,
)
from zero_sdk.network import Network
from zero_sdk.utils import hash_string
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
        version,
        date_created,
        network,
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
            if self.client_id is not None:
                return method(self, *args, **kwargs)
            else:
                self._init_wallet()
                raise Exception(
                    "Wallet is not initialized, call 'create_wallet, init_wallet or recover_wallet' methods to configure wallet"
                )

        return wrapper

    @_validate_wallet
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

    def get_locked_tokens(self):
        endpoint = f"{Endpoints.GET_LOCKED_TOKENS}?client_id={self.client_id}"
        empty_return_value = {"locked_tokens": []}
        res = self._consensus_from_workers(
            "sharders", endpoint, empty_return_value=empty_return_value
        )
        return res

    def get_user_pools(self):
        endpoint = f"{Endpoints.GET_USER_POOLS}?client_id={self.client_id}"
        empty_return_value = {"pools": {}}
        res = self._consensus_from_workers(
            "sharders", endpoint, empty_return_value=empty_return_value
        )
        return res

    def create_read_pool(self):
        payload = json.dumps({"name": "new_read_pool", "input": None})
        res = self._execute_smart_contract(payload)
        return res

    def _execute_smart_contract(self, payload, to_client_id=None, transaction_value=0):
        if not to_client_id:
            to_client_id = STORAGE_SMART_CONTRACT_ADDRESS
        return self._submit_transaction(
            to_client_id, transaction_value, payload, TransactionType.SMART_CONTRACT
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

        res = self._execute_smart_contract(payload, transaction_value=lock_tokens)
        return res

    def list_allocations(self):
        url = f"{Endpoints.SC_REST_ALLOCATIONS}?client={self.client_id}"
        res = self._consensus_from_workers("sharders", url)
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

    # ____________________________
    # END HERE
    # ____________________________

    # def _create

    def sign(self, payload):
        return sign_payload(self.private_key, payload)

    @_validate_wallet
    def add_tokens(self, amount=1) -> object:
        url = f"{self.network.url}/miner01/v1/transaction/put"
        headers = {"Content-Type": "application/json; charset=utf-8"}

        # Creation date
        creation_date = int(time())

        # Transaction data hash
        transaction_data_string = '{"name":"pour","input":{},"name":null}'
        transaction_data_hash = hash_string(transaction_data_string)

        # Main hash payload
        payload_string = f"{creation_date}:{self.client_id}:{self.network.remote_client_id}:10000000000:{transaction_data_hash}"
        hashed_payload = hash_string(payload_string)

        # signature = heroku_sign(hashed_payload)
        signature = self.sign(self.private_key, hashed_payload)
        if signature == False:
            raise Exception("There was an error signing the transaction")

        # Build raw data
        data = {
            "hash": hashed_payload,
            "signature": signature,
            "version": "1.0",
            "client_id": self.client_id,
            "creation_date": creation_date,
            "to_client_id": self.network.remote_client_id,
            "transaction_data": transaction_data_string,
            "transaction_fee": 0,
            "transaction_type": 1000,
            "transaction_value": amount * 10000000000,
            "txn_output_hash": "",
            "public_key": self.public_key,
        }

        res = requests.post(url, json=data, headers=headers)
        error_message = "An error occurred adding tokens to wallet"
        res = self._check_status_code(res, error_message)

        return res

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
            config.get("version"),
            config.get("date_created"),
            network,
        )

    def __repr__(self):
        return f"Wallet(config, network)"

    def __str__(self):
        return f"client_id: {self.client_id} \nnetwork_url: {self.network.hostname}"
