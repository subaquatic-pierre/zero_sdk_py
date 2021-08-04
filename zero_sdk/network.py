import json
import requests
from zero_sdk.connection_base import ConnectionBase
from zero_sdk.const import Endpoints
from zero_sdk.workers import Blobber, Miner, Sharder
from zero_sdk.utils import hostname_from_config_obj


class Network(ConnectionBase):
    def __init__(
        self, hostname, miners, sharders, preferred_blobbers, min_confirmation
    ) -> None:
        self.hostname: str = hostname
        self.miners: list = miners
        self.sharders: list = sharders
        self.preferred_blobbers: list = preferred_blobbers
        self.min_confirmation: int = min_confirmation

    def get_chain_stats(self):
        endpoint = Endpoints.GET_CHAIN_STATS
        res = self._get_consensus_from_workers("sharders", endpoint)
        return res

    def get_block_by_hash(self, block_id):
        endpoint = f"{Endpoints.GET_BLOCK_INFO}?block={block_id}"
        res = self._get_consensus_from_workers("sharders", endpoint)
        return res

    def get_block_by_round(self, round_num):
        endpoint = f"{Endpoints.GET_BLOCK_INFO}?round={round_num}"
        res = self._get_consensus_from_workers("sharders", endpoint)
        return res

    def get_latest_finalized_block(self):
        endpoint = Endpoints.GET_LATEST_FINALIZED_BLOCK
        res = self._get_consensus_from_workers("sharders", endpoint)
        return res

    def get_latest_finalized_magic_block(self):
        endpoint = Endpoints.GET_LATEST_FINALIZED_MAGIC_BLOCK
        res = self._get_consensus_from_workers("sharders", endpoint)
        return res

    def get_latest_finalized_magic_block_summary(self):
        endpoint = Endpoints.GET_LATEST_FINALIZED_MAGIC_BLOCK_SUMMARY
        res = self._get_consensus_from_workers("miners", endpoint)
        return res

    def check_transaction_status(self, hash):
        endpoint = f"{Endpoints.CHECK_TRANSACTION_STATUS}?hash={hash}"
        res = self._get_consensus_from_workers("sharders", endpoint)
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


def request_dns_workers(url, worker):
    res = requests.get(f"{url}/{Endpoints.NETWORK_DNS}")

    if res.status_code != 200:
        raise Exception(f"An error occured requesting workers - {res.text}")

    workers = res.json().get(worker)
    if not workers:
        raise Exception(f"No {worker} found")

    return workers
