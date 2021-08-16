from datetime import timedelta
import json
import random
import string
from time import time
import yaml
import secrets
from pathlib import Path
from hashlib import sha3_256
from bip39 import encode_bytes
import requests

from zerochain.const import Endpoints


def generate_random_letters(num_letters=5):
    letters = string.ascii_lowercase
    rand_letters = "".join(random.choices(letters, k=num_letters))
    return rand_letters


def pprint(dict):
    print(json.dumps(dict, indent=4))


def hash_string(payload_string):
    hash_object = sha3_256(bytes(payload_string, "utf-8"))
    return f"{hash_object.hexdigest()}"


def get_project_root():
    return Path(__file__).parent.resolve().parent.resolve()


def get_home_path():
    return f"{Path().home()}"


def hostname_from_config_obj(network_config) -> str:
    split = network_config["block_worker"].split("/")
    new_split = split[:-1]
    url = "/".join(new_split)
    return url


def from_json(filename) -> object:
    data = None
    with open(filename, "r") as f:
        data = json.load(f)

    verified_data = verify_data(data)
    return verified_data


def from_yaml(filename) -> object:
    data = None
    with open(filename, "r") as f:
        data = yaml.safe_load(f)

    verified_data = verify_data(data)
    return verified_data


def verify_data(data):
    if data == None:
        raise Exception("No data loaded")
    else:
        return data


def generate_mnemonic():
    byte_array = secrets.token_bytes(32)
    mnemonic = encode_bytes(bytearray(byte_array))
    return mnemonic


def timer(f):
    def wrapper(*args, **kwargs):
        start_time = time()
        res = f(*args, **kwargs)
        end_time = time()
        total_time = end_time - start_time
        print("Total Time: ", total_time)
        return res

    return wrapper


def create_client_util(data, network):
    from zerochain.client import Client

    return Client.from_object(data, network)


def create_allocation(allocation_id, client):
    from zerochain.allocation import Allocation

    return Allocation(allocation_id, client)


def get_duration_nanoseconds(days=0, hours=0, minutes=0, seconds=0):
    seconds = int(
        timedelta(
            days=days, hours=hours, minutes=minutes, seconds=seconds
        ).total_seconds()
    )

    return seconds * 1000000000


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
