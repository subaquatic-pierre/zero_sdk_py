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

info = network.get_worker_stats("sharders")
worker_id = network.get_worker_id("https://beta.0chain.net/sharder01")

# info = aloc.get_blobber_stats(
#     blobber_id="144a94640cb78130434a79a7a12d0b2c85f819e3ea8856db31c7fde30c30a820"
# )

# info = wallet.get_vesting_pool_config()

pprint(info)
print(worker_id)
# req, data = wallet.add_tokens()

# print("Req Num: ", req)
