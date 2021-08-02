import json
from zero_sdk.network import Network
from zero_sdk.utils import get_home_path
from zero_sdk.wallet import Wallet
from zero_sdk.allocation import Allocation
from zero_sdk.config import default_network_config_obj
from zero_sdk.utils import pprint
from reedsolo import RSCodec

network = Network.from_object(default_network_config_obj)
chain_stats = network.get_chain_stats()
latest_block = network.get_latest_finalized_block()
block_hash = latest_block["hash"]
block = network.get_block(block_hash)

pprint(chain_stats)
pprint(block)


# rsc = RSCodec(2)

# wallet = Wallet()
# main_alloc = Allocation(config.MAIN_ALLOCATION_ID, wallet, config.STORAGE_ADDRESS)

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
