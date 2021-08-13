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

txn_hash = "17297e21e21c59b32de70f082a8668166cc9cb06eb5071abd2907089c45c7238"
aloc_id = "fd1835c64f4b96f87ccfb478712a8fb09149ad38bbfada9c9e2c9986f62c7202"
send_wallet_id = "f203b553bad7e0ac78a4561d39acbe5021d855433a0b8a2094195b02b00216ce"
vp_id = "2bba5b05949ea59c80aed3ac3474d7379d3be737e8eb5a968c52295e48333ead:vestingpool:ce4387472f04c3f5514134691d88663fde4187d1db32509c9ee8421ee95a1358"
miner_id = "99dfe67a348281ba40a979db7e5cffabdedea3c432bb41079d0fbc6e2d554143"

network = Network.from_object(default_network_config_obj)
wallet = Wallet.from_object(default_wallet_config_obj, network)
aloc = Allocation(aloc_id, wallet)

data = aloc.get_allocation_info()

data = aloc.list_blobbers()
pprint(data)

print("ALOC BY ID:")
data = aloc.get_blobber_info(
    blobber_id="144a94640cb78130434a79a7a12d0b2c85f819e3ea8856db31c7fde30c30a820"
)
pprint(data)

print("BY URL:")
data = aloc.get_blobber_stats(blobber_url="http://beta.0chain.net:31301")
pprint(data)
