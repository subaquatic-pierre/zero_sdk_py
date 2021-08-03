import json
from zero_sdk.network import Network
from zero_sdk.utils import get_home_path
from zero_sdk.wallet import Wallet
from zero_sdk.allocation import Allocation
from zero_sdk.config import default_network_config_obj, default_wallet_config_obj
from zero_sdk.utils import pprint

network = Network.from_object(default_network_config_obj)
wallet = Wallet.from_object(default_wallet_config_obj, network)

balance = wallet.get_balance()
chain_stats = network.get_chain_stats()

print(balance)
