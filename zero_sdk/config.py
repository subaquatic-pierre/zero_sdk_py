import os
from pathlib import Path
from zero_sdk.utils import from_json

PROJECT_ROOT = Path(__file__).resolve().parent.resolve().parent.resolve()

default_network_obj = from_json(
    os.path.join(PROJECT_ROOT, "default_config/network.json")
)

default_wallet_obj = from_json(os.path.join(PROJECT_ROOT, "default_config/wallet.json"))
