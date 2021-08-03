import os
from zero_sdk.utils import get_project_root

from zero_sdk.network import Network
from zero_sdk.wallet import Wallet
from zero_sdk.workers import Miner, Sharder, Blobber

TEST_DIR = os.path.join(get_project_root(), "tests")


def build_wallet():
    network = build_network(50)
    wallet = Wallet(
        client_id="client_id",
        client_key="client_key",
        public_key="public_key",
        private_key="private_key",
        mnemonics="mnemonics",
        version="version",
        date_created="date_created",
        network=network,
    )
    return wallet


def build_network(min_confirmations):
    placeholder_workers = [
        "http://worker01.com",
        "http://worker02.com",
        "http://worker03.com",
    ]
    miners = [Miner(url) for url in placeholder_workers]
    sharders = [Sharder(url) for url in placeholder_workers]
    blobbers = [Blobber(url) for url in placeholder_workers]
    return Network(
        "http://placehoder.com", miners, sharders, blobbers, min_confirmations
    )
