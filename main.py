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
txn_hash = "17297e21e21c59b32de70f082a8668166cc9cb06eb5071abd2907089c45c7238"
aloc_id = "fd1835c64f4b96f87ccfb478712a8fb09149ad38bbfada9c9e2c9986f62c7202"
send_client_id = "f203b553bad7e0ac78a4561d39acbe5021d855433a0b8a2094195b02b00216ce"
vp_id = "2bba5b05949ea59c80aed3ac3474d7379d3be737e8eb5a968c52295e48333ead:vestingpool:ce4387472f04c3f5514134691d88663fde4187d1db32509c9ee8421ee95a1358"
miner_id = "99dfe67a348281ba40a979db7e5cffabdedea3c432bb41079d0fbc6e2d554143"

network = Network.from_object(default_network_config_obj)
client = Client.from_object(default_client_config_obj, network)
aloc = Allocation(aloc_id, client)

# data = client.blobber_unlock_token(
#     "9c3b29784c7874d6cc95f678a94118469af058feffeee9daec4baabfcfdaeadd",
#     "6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d7",
# )
data = client.unlock_token(
    "3be2931a1a45937f263ca49057a7c56ab4b9abac8e31102b4338191034bd3a76"
)
list = client.list_lock_token()
pprint(list)
data = client.get_balance("human")
pprint(data)


# from reedsolo import RSCodec


# rsc = RSCodec(2)

# client = Client()
# main_alloc = Allocation(config.MAIN_ALLOCATION_ID, client, config.STORAGE_ADDRESS)

# path = f"{get_home_path()}/.zcn/uploads/1.txt"
# upload_res = main_alloc.upload_file(path)

# for res in upload_res:
#     print(res.text)


# info = main_alloc.get_allocation_info()
# print(json.dumps(info, indent=4))

# new_file = f"{get_home_path()}/.zcn/downloads/downloaded_stack_page.txt"

# download_res = main_alloc.download_file("/stack_page.txt", new_file)

# encoded_data = "".join(results)
# data = b""
# for res in download_res:
#     data = data + res

# decoded_data = rsc.decode(data)
# print(decoded_data[0])

# with open(new_file, "wb") as file:
#     file.write(data)
