import json
import requests
from zero_sdk.connection_base import ConnectionBase
from zero_sdk.const import Endpoints
from zero_sdk.workers import Blobber, Miner, Sharder
from zero_sdk.utils import hostname_from_config_obj


class Network(ConnectionBase):
    def __init__(self, hostname, miners, sharders, preferred_blobbers):
        self.hostname = hostname
        self.miners = miners
        self.sharders = sharders
        self.preferred_blobbers = preferred_blobbers

    def _request_from_sharders(self, endpoint):
        res = None
        for sharder in self.sharders:
            url = f"{sharder.url}/{endpoint}"
            res = self._request("GET", url)
            if res:
                return res

        if not res:
            raise Exception("No chain stats found")

        return res

    def get_chain_stats(self):
        endpoint = Endpoints.GET_CHAIN_STATS
        res = self._request_from_sharders(endpoint)
        return res

    def get_recent_finalized(self):
        endpoint = Endpoints.GET_CHAIN_STATS
        res = self._request_from_sharders(endpoint)
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

        return Network(hostname, miners, sharders, preferred_blobbers)

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
