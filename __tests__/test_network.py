from unittest.case import TestCase
from zero_sdk.network import Network
from setup import config
from zero_sdk.utils import from_yaml, get_home_path

default_network_config = from_yaml(f"{get_home_path()}/.zcn/network_config.json")


class TestNetwork(TestCase):
    def setUp(self) -> None:
        self.network = Network(default_network_config)
        return super().setUp()

    def test_no_miners(self):
        """Miners were loaded"""
        self.assertTrue(len(self.network.miners) > 0)

    def test_no_miners(self):
        """Sharders were loaded"""
        self.assertTrue(len(self.network.sharders) > 0)

    def test_no_miners(self):
        """Base network url loaded correctly"""
        self.assertTrue(self.network.url == config.BASE_URL)

    def test_no_miners(self):
        """Remote client ID loaded"""
        self.assertTrue(self.network.remote_client_id is not None)
