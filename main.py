import json
from zero_sdk.network import Network
from zero_sdk.utils import get_home_path
from zero_sdk.wallet import Wallet
from zero_sdk.allocation import Allocation
from zero_sdk.config import default_network_config_obj, default_wallet_config_obj
from zero_sdk.utils import pprint
from zero_sdk.bls import genereate_keys

# network = Network.from_object(default_network_config_obj)
# wallet = Wallet.from_object(default_wallet_config_obj, network)

# locked_tockens = wallet.get_locked_tokens()

# print(locked_tockens)

keys = genereate_keys()

print(json.dumps(keys, indent=4))
