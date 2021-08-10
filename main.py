import json
from math import inf
from time import sleep
from zero_sdk.workers import Blobber
from zero_sdk import allocation
from zero_sdk.wallet import Wallet
from zero_sdk.utils import (
    generate_mnemonic,
    generate_random_letters,
    get_home_path,
    hash_string,
)

# from zero_sdk.wallet import Wallet
from zero_sdk.allocation import Allocation
from zero_sdk.config import default_network_config_obj, default_wallet_config_obj
from zero_sdk.utils import pprint
from zero_sdk.network import Network

# txn_hash = "17297e21e21c59b32de70f082a8668166cc9cb06eb5071abd2907089c45c7238"
aloc_id = "296896621095a9d8a51e6e4dba2bdb5661ea94ffd8fdb0a084301bffd81fe7e6"

network = Network.from_object(default_network_config_obj)
wallet = Wallet.from_object(default_wallet_config_obj, network)
aloc = Allocation(aloc_id, wallet)

write_pool = aloc.get_write_pool_info()
print(write_pool)

read_pool = aloc.get_read_pool_info()
print(read_pool)
# hash = res["entity"]["hash"]
