import json
from zero_sdk.connection_base import ConnectionBase
import requests
from zero_sdk.const import Endpoints
from zero_sdk.miner import Miner
from zero_sdk.sharder import Sharder
from zero_sdk.utils import hostname_from_config_obj


class Network(ConnectionBase):
    def __init__(self, hostname, miners, sharders, blobbers):
        self.hostname = hostname
        self.miners = miners
        self.sharders = sharders
        self.blobbers = blobbers

    @staticmethod
    def from_object(config_obj):
        hostname = hostname_from_config_obj(config_obj)
        miners = request_dns_workers(hostname, "miners")
        sharders = request_dns_workers(hostname, "sharders")
        blobbers = []
        return Network(hostname, miners, sharders, blobbers)

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

    if worker == "miner":
        return [Miner(url) for url in workers]
    elif worker == "sharder":
        return [Sharder(url) for url in workers]
