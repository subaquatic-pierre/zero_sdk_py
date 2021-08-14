import json
from time import time, sleep

from zerochain.const import Endpoints
from zerochain.utils import hash_string
from zerochain.connection import ConnectionBase
from zerochain.exceptions import TransactionError
from zerochain.const import STORAGE_SMART_CONTRACT_ADDRESS


class Transaction(ConnectionBase):
    def __init__(
        self,
        sc_address,
        transaction_name,
        transaction_type,
        input,
        value,
        wallet,
        raise_exception,
        timeout=5,
    ) -> None:
        self.sc_address = sc_address
        self.input = input
        self.name = transaction_name
        self.type = transaction_type
        self.value = value * 10000000000
        self.network = wallet.network
        self.wallet = wallet
        self.status = 0
        self.hash = None
        self.response_data = None
        self.confirmation_data = None
        self.timeout = timeout
        self.raise_exception = raise_exception

    def _submit_transaction(self, payload):
        hash_payload = hash_string(payload)
        ts = int(time())

        hashdata = f"{ts}:{self.wallet.client_id}:{self.sc_address}:{self.value}:{hash_payload}"

        self.hash = hash_string(hashdata)
        signature = self.wallet.sign(self.hash)

        data = json.dumps(
            {
                "client_id": self.wallet.client_id,
                "public_key": self.wallet.public_key,
                "transaction_value": self.value,
                "transaction_data": payload,
                "transaction_type": self.type,
                "creation_date": ts,
                "to_client_id": self.sc_address,
                "hash": self.hash,
                "transaction_fee": 0,
                "signature": signature,
                "version": "1.0",
            }
        )

        headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
        self.response_data = self._consensus_from_workers(
            "miners",
            endpoint=Endpoints.PUT_TRANSACTION,
            method="POST",
            data=data,
            headers=headers,
        )
        try:
            response_hash = self.response_data.get("entity").get("hash")
        except:
            print(self.response_data)
            raise TransactionError("Response doesnt contain hash")

        if response_hash != self.hash:
            raise TransactionError("Request hash and response hash do not match")

        return self.response_data

    def execute(self):
        if not self.name:
            payload = self.input
        else:
            payload = json.dumps({"name": self.name, "input": self.input})

        return self._submit_transaction(
            payload,
        )

    def validate(self, hash=None):
        if not hash:
            hash = self.hash
        for i in range(10):
            if i == self.timeout:
                break
            sleep(1)
            try:
                self.confirmation_data = self.network.check_transaction_status(hash)
                self.status = self.confirmation_data.get("transaction_status")
            except:
                pass

            if self.status == 1:
                break

        if self.status == 1:
            return self.confirmation_data

        if self.raise_exception:
            raise TransactionError("Transaction could to be confirmed")
        else:
            return self.response_data
