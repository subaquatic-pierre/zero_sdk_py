import os
from unittest.mock import MagicMock

from tests.mock_response import MockResponse

from zerochain.utils import get_project_root, from_json
from zerochain.network import Network
from zerochain.client import Client
from zerochain.workers import Miner, Sharder, Blobber

TEST_DIR = os.path.join(get_project_root(), "tests")


def build_client():
    network = build_network(50)
    client = Client(
        client_id="31680e6a4fa9bb9466b7c46d1c853026a672cb913ebaae8e4af9539b15cbe5d8",
        client_key="d2a87be4da594dd01fb1be18fad4dd2d2341be4ae5b5584229121cbe91b1e411",
        public_key="812c1c446a6820f84d097ffeef684054606b7c9ae401a85bf0a71de96126e222777f7c69b282d46bfbbc735ca736502beac080446f27d4a5b2b22bf04459b500",
        private_key="d2a87be4da594dd01fb1be18fad4dd2d2341be4ae5b5584229121cbe91b1e411   ",
        mnemonic="sentence believe vague meat slender blind vibrant embrace gloom very dust enrich salon ginger ripple ethics hard name vital hurry digital pistol also lawsuit",
        version="version",
        date_created="date_created",
        network=network,
    )
    return client


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


def create_mock_response(path=None, data=None, format="path"):
    if not path and not data:
        raise TypeError("Atleast filename or data object needs to be passed")

    if format == "path":
        res_obj = from_json(os.path.join(TEST_DIR, f"__mocks__/{path}"))
        mock_response = MagicMock(return_value=res_obj)
        return mock_response

    else:
        mock_response = MagicMock(return_value=data)
        return mock_response
