import json
from pathlib import Path
import os
from zerochain.connection import ConnectionBase

import requests
from zerochain.workers import Blobber
from zerochain.const import Endpoints, StorageEndpoints
from zerochain.utils import generate_random_letters, hash_string
from zerochain.actions import blobber, allocation

file_info = {"size": "", "actual_size": 0, "hash": "", "type": ""}


def get_reference_lookup(allocation_id, path):
    return hash_string(f"{allocation_id}:{path}")


class ListRequest:
    def __init__(
        self, allocation, remote_file_path, remote_file_path_hash=None
    ) -> None:
        self.alloction_id = allocation.id
        self.blobbers = allocation.blobbers
        self.tx = allocation.tx
        self.remote_file_path_hash = remote_file_path_hash
        self.remote_file_path = remote_file_path

    def make_request(self):
        url = f'{self.blobbers[0].url}/v1/file/referencepath/{self.id}?paths=["{path}"]'
        print(url)
        res = requests.get(url)
        try:
            return res.data
        except:
            return res.text


class Allocation(ConnectionBase):
    def __init__(self, allocation_id, client) -> None:
        blobber_list = blobber.list_blobbers_by_allocation_id(client, allocation_id)
        self.id = allocation_id
        self.tx = allocation.get_allocation_tx(client, allocation_id)
        self.client = client
        self.blobbers = [
            Blobber(blobber_node["url"], blobber_node["id"])
            for blobber_node in blobber_list
        ]

    def list_blobbers(self):
        return self.blobbers

    def list_all_files(self):
        path = "/"

        path_hash = hash_string(f"{self.id}:{path}")

        # params = f"?auth_token=&path_hash={path_hash}"
        endpoint = Endpoints.ALLOCATION_FILE_LIST + self.id
        url = self.blobbers[0]["url"] + endpoint

        print(url)

        headers = {
            "X-App-Client-Id": self.client.id,
            "X-App-Client-Key": self.client.client_key,
        }

        try:
            data = json.loads(res.text)
            return data
        except:
            return res.text

    def get_list_request(self, path, headers, url, path_hash):
        req = requests.Request("GET", url=url, headers=headers)
        req.params = {"auth_token": None, "path_hash": path_hash}
        prep = req.prepare()
        print(prep.url)
        s = requests.Session()
        res = s.send(prep)

        return prep

    def _perform_requests(self, workers, req):
        results = []

        return results

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

    def from_object(aloc_obj, client):
        aloc_id = aloc_obj["id"]
        aloc = Allocation(aloc_id, client)
        for key, value in aloc_obj.items():
            setattr(aloc, key, value)

        return aloc

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
