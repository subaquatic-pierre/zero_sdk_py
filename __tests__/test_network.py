from zero_sdk.network import Network
from setup import config
from zero_sdk.utils import from_yaml, get_home_path

default_network_config = from_yaml(f"{get_home_path()}/.zcn/network_config.json")


# Test network has miners
network = Network(default_network_config)
assert len(network.miners) > 0, "No miners were loaded"

# Test network has sharders
network = Network(default_network_config)
assert len(network.sharders) > 0, "No sharders were loaded"

# Test network url
network = Network(default_network_config)
assert network.url == config.BASE_URL, "Base network url not loaded correctly"

# Test network has remote client ID
network = Network(default_network_config)
assert network.remote_client_id is not None, "Remote client ID not loaded"
