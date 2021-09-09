import json
from tests.test_blobber import BLOBBER_ID
from time import sleep
from zerochain.client import Client
from zerochain.utils import (
    generate_mnemonic,
    generate_random_letters,
    get_home_path,
    hash_string,
)

# from zerochain.client import Client
from zerochain.allocation import Allocation
from zerochain.config import default_network_config_obj, default_client_config_obj
from zerochain.utils import pprint
from zerochain.network import Network

blobber_id = "144a94640cb78130434a79a7a12d0b2c85f819e3ea8856db31c7fde30c30a820"
blobber_url = "http://beta.0chain.net:31301"
aloc_id = "d5284fcf79576006f37888b13b8a910cd87a365d76315952532656f15ecec25c"
send_client_id = "f203b553bad7e0ac78a4561d39acbe5021d855433a0b8a2094195b02b00216ce"
vp_id = "2bba5b05949ea59c80aed3ac3474d7379d3be737e8eb5a968c52295e48333ead:vestingpool:ce4387472f04c3f5514134691d88663fde4187d1db32509c9ee8421ee95a1358"
miner_id = "99dfe67a348281ba40a979db7e5cffabdedea3c432bb41079d0fbc6e2d554143"

network = Network.from_object(default_network_config_obj)
client = Client.from_object(default_client_config_obj, network)

aloc = Allocation(
    "d5284fcf79576006f37888b13b8a910cd87a365d76315952532656f15ecec25c", client
)

res = aloc.list_files("/")
pprint(res)
