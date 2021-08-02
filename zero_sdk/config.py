import os
from pathlib import Path
from zero_sdk.utils import from_json, from_yaml

PROJECT_ROOT = Path(__file__).resolve().parent.resolve().parent.resolve()
DEFUALT_PUBLIC_URL = "https://beta.0chain.net"

# Change default paths to home dir in production
default_network_config_obj = from_yaml(
    os.path.join(PROJECT_ROOT, "zero_sdk/default_config/network.yaml")
)
default_wallet_config_obj = from_json(
    os.path.join(PROJECT_ROOT, "zero_sdk/default_config/wallet.json")
)
