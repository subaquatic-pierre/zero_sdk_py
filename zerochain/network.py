from zerochain.connection import ConnectionBase
from zerochain.workers import Blobber, Miner, Sharder
from zerochain.utils import hostname_from_config_obj, request_dns_workers


class Network(ConnectionBase):
    def __init__(
        self, hostname, miners, sharders, preferred_blobbers, min_confirmation
    ) -> None:
        self.hostname: str = hostname
        self.miners: list = miners
        self.sharders: list = sharders
        self.preferred_blobbers: list = preferred_blobbers
        self.min_confirmation: int = min_confirmation

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
