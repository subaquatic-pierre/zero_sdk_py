import json
from pathlib import Path
import os

from zerochain.utils import generate_random_letters


class Allocation:
    def __init__(self, id, client) -> None:
        self.id = id
        self.client = client

    def save(self, allocation_name=None):
        if not allocation_name:
            allocation_name = generate_random_letters()

        data = self.get_allocation_info()

        with open(
            os.path.join(
                Path.home(), f".zcn/test_allocations/allocation_{allocation_name}.json"
            ),
            "w",
        ) as f:
            f.write(json.dumps(data, indent=4))

    def __str__(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "client_id": self.client.id,
                "network_url": self.client.network.hostname,
            },
            indent=4,
        )

    def __repr__(self) -> str:
        return f"Allocation(id, client)"
