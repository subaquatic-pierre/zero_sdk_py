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

trans_client = {
    "client_id": "f203b553bad7e0ac78a4561d39acbe5021d855433a0b8a2094195b02b00216ce",
    "public_key": "5e8fd56201dccf39ba6dac429a3b622e9436d40836645b779d944c348dd7980850eabdbb552af5f6734cc23cb4d1c81b0d0039f1e211468a7239b4c06c9d419d",
}

# add = client.add_curator(
#     client.id, "183ec3c9f1767d2495415ff00ebfa2871624232758ae65a966d038f4dfbef369"
# )

data = client.transfer_allocation(
    trans_client["client_id"],
    trans_client["public_key"],
    "183ec3c9f1767d2495415ff00ebfa2871624232758ae65a966d038f4dfbef369",
)

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
