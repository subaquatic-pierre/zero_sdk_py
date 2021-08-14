import os
from pathlib import Path
from zerochain.utils import from_json, from_yaml, get_home_path

PROJECT_ROOT = Path(__file__).resolve().parent.resolve().parent.resolve()
HOME_PATH = get_home_path()
DEFUALT_PUBLIC_URL = "https://beta.0chain.net"

# Change default paths to home dir in production
default_network_config_obj = from_yaml(os.path.join(HOME_PATH, ".zcn/config.yaml"))
default_wallet_config_obj = from_json(os.path.join(HOME_PATH, ".zcn/wallet.json"))
