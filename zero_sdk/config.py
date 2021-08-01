import os
from pathlib import Path
from zero_sdk.utils import from_json

PROJECT_ROOT = Path(__file__).resolve().parent.resolve().parent.resolve()
PUBLIC_URL = "https://beta.0chain.net"

# Change default paths to home dir in production
default_network_obj = from_json(
    os.path.join(PROJECT_ROOT, "default_config/network.json")
)
default_wallet_obj = from_json(os.path.join(PROJECT_ROOT, "default_config/wallet.json"))
