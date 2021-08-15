import os
import json
from zerochain.config import PROJECT_ROOT
import requests

from zerochain.connection import ConnectionBase
from zerochain.const import Endpoints, STORAGE_SMART_CONTRACT_ADDRESS
from zerochain.workers import Blobber, Miner, Sharder
from zerochain.utils import hostname_from_config_obj
from zerochain.utils import generate_mnemonic, create_client
from zerochain.bls import generate_keys


class Network(ConnectionBase):
    def __init__(
        self, hostname, miners, sharders, preferred_blobbers, min_confirmation
    ) -> None:
        self.hostname: str = hostname
        self.miners: list = miners
        self.sharders: list = sharders
        self.preferred_blobbers: list = preferred_blobbers
        self.min_confirmation: int = min_confirmation

    def list_network_dns(self):
        return request_dns_workers(url=self.hostname)

    def list_miners(self):
        endpoint = Endpoints.SC_MINERS_STATS
        res = self._consensus_from_workers("miners", endpoint)
        try:
            miners = res.get("Nodes")
            return miners
        except:
            return res

    def get_miner_config(self):
        endpoint = Endpoints.SC_CONFIGS
        res = self._consensus_from_workers("sharders", endpoint)
        return res

    def get_node_stats(self, node_id=None):
        if not node_id:
            raise Exception("Please provide node ID")
        endpoint = f"{Endpoints.SC_NODE_STAT}?id={node_id}"
        res = self._consensus_from_workers("sharders", endpoint)
        return res

    def list_sharders(self):
        res = self.get_latest_finalized_magic_block()
        try:
            sharders = res.get("magic_block").get("sharders").get("nodes")
            return sharders
        except:
            return {"error": "not found"}

    def get_miner_list(self):
        endpoint = Endpoints.SC_MINERS_STATS
        res = self._consensus_from_workers("sharders", endpoint)
        return res

    def get_chain_stats(self):
        endpoint = Endpoints.GET_CHAIN_STATS
        res = self._consensus_from_workers("sharders", endpoint)
        return res

    def get_block_by_hash(self, block_id):
        endpoint = f"{Endpoints.GET_BLOCK_INFO}?block={block_id}"
        res = self._consensus_from_workers("sharders", endpoint)
        return res

    def get_block_by_round(self, round_num):
        endpoint = f"{Endpoints.GET_BLOCK_INFO}?round={round_num}"
        res = self._consensus_from_workers("sharders", endpoint)
        return res

    def get_latest_finalized_block(self):
        endpoint = Endpoints.GET_LATEST_FINALIZED_BLOCK
        res = self._consensus_from_workers("sharders", endpoint)
        return res

    def get_latest_finalized_magic_block(self):
        endpoint = Endpoints.GET_LATEST_FINALIZED_MAGIC_BLOCK
        res = self._consensus_from_workers("sharders", endpoint)
        return res

    def get_latest_finalized_magic_block_summary(self):
        endpoint = Endpoints.GET_LATEST_FINALIZED_MAGIC_BLOCK_SUMMARY
        res = self._consensus_from_workers("miners", endpoint)
        return res

    def check_transaction_status(self, hash):
        endpoint = f"{Endpoints.CHECK_TRANSACTION_STATUS}?hash={hash}"
        res = self._consensus_from_workers("sharders", endpoint)
        return res

    def get_worker_stats(self, worker):
        details = {}
        workers = self._get_workers(worker)
        for worker in workers:
            url = f"{worker.url}/_nh/whoami"
            res = self._request(url)
            valid_data = self._check_status_code(res)
            details.setdefault(worker.url, valid_data)

        return details

    def get_worker_id(self, worker_url):
        details = {}
        url = f"{worker_url}/_nh/whoami"
        res = self._request(url)
        valid_data = self._check_status_code(res)
        details.setdefault(worker_url, valid_data)

        return details

    def get_storage_smartcontract_for_key(self, key_name, key_value):
        payload = json.dumps(
            {
                "key": f"{key_name}:{key_value}",
                "sc_address": STORAGE_SMART_CONTRACT_ADDRESS,
            }
        )
        res = self._consensus_from_workers(
            "sharders", Endpoints.GET_SCSTATE, data=payload
        )
        return res

    def create_client(self):
        mnemonic = generate_mnemonic()
        keys = self._create_keys(mnemonic)
        res = self._register_client(keys)
        data = {
            "client_id": res["id"],
            "client_key": keys["public_key"],
            "keys": [
                {
                    "public_key": keys["public_key"],
                    "private_key": keys["private_key"],
                }
            ],
            "mnemonic": mnemonic,
            "version": res["version"],
            "date_created": res["creation_date"],
        }

        client = create_client(data, self)
        return client

    def restore_client(self, mnemonic):
        keys = self._create_keys(mnemonic)
        res = self._register_client(keys)
        return res

    def _create_keys(self, mnemonic):
        keys = generate_keys(mnemonic)
        return keys

    def _register_client(self, keys):
        payload = json.dumps(
            {
                "id": keys["client_id"],
                "version": None,
                "creation_date": None,
                "public_key": keys["public_key"],
            }
        )
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        res = self._consensus_from_workers(
            "miners",
            endpoint=Endpoints.REGISTER_CLIENT,
            method="PUT",
            data=payload,
            headers=headers,
            min_confirmation=10,
        )
        return res

    def json(self):
        return {
            "hostname": self.hostname,
            "miners": [worker.url for worker in self.miners],
            "sharders": [worker.url for worker in self.sharders],
            "preferred_blobbers": [worker.url for worker in self.preferred_blobbers],
        }

    @staticmethod
    def from_object(config_obj, hostname=None):
        if not hostname:
            hostname = hostname_from_config_obj(config_obj)
        miners = [Miner(url) for url in request_dns_workers(hostname, "miners")]
        sharders = [Sharder(url) for url in request_dns_workers(hostname, "sharders")]

        # Todo: Error check blobber load
        preferred_blobbers = [
            Blobber(url) for url in config_obj.get("preferred_blobbers")
        ]
        min_confirmation = config_obj["min_confirmation"]

        return Network(hostname, miners, sharders, preferred_blobbers, min_confirmation)

    def __str__(self) -> str:
        return f"hostname: {self.hostname}"

    def __repr__(self) -> str:
        return f"Network()"


def request_dns_workers(url, worker=None):
    res = requests.get(f"{url}/{Endpoints.NETWORK_DNS}")

    if res.status_code != 200:
        raise ConnectionError(f"An error occured requesting workers - {res.text}")

    if not worker:
        return res.json()

    workers = res.json().get(worker)
    if not workers:
        raise KeyError(f"No {worker} found")

    return workers
