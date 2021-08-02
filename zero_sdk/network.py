import json
from zero_sdk.connection_base import ConnectionBase
import requests
from zero_sdk.const import Endpoints
from zero_sdk.workers import Blobber, Miner, Sharder
from zero_sdk.utils import hostname_from_config_obj


class Network(ConnectionBase):
    def __init__(self, hostname, miners, sharders, preferred_blobbers):
        self.hostname = hostname
        self.miners = miners
        self.sharders = sharders
        self.preferred_blobbers = preferred_blobbers

    def json(self):
        network_dict = {
            "hostname": self.hostname,
            "miners": [worker.url for worker in self.miners],
            "sharders": [worker.url for worker in self.sharders],
            "preferred_blobbers": [worker.url for worker in self.preferred_blobbers],
        }
        return json.dumps(network_dict, indent=4)

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
