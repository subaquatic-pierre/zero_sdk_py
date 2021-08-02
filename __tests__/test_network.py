from unittest.case import TestCase
from zero_sdk.network import Network
from zero_sdk.utils import from_yaml, get_project_root

default_network_config = from_yaml(
    f"{get_project_root()}/__tests__/fixtures/default_network.yaml"
)


class TestNetworkInit(TestCase):
    def test_from_object(self):
        """Test network can be instantiated from standard config object"""
        network = Network.from_object(default_network_config)
        self.assertTrue(network)

    def test_error_from_object(self):
        """Test an error is thrown on incorrect config object sent to from object method"""
        with self.assertRaises(Exception):
            network = Network.from_object({})
            self.assertTrue(network)


class TestNetworkAttributes(TestCase):
    def setUp(self) -> None:
        self.network = Network.from_object(default_network_config)
        return super().setUp()

    def test_has_miners(self):
        """Test network has atleast one miner"""
        miners = self.network.miners
        self.assertGreater(len(miners), 0)

    def test_has_sharders(self):
        """Test network has atleast one shrader"""
        sharders = self.network.sharders
        self.assertGreater(len(sharders), 0)


class TestNetworkMethods(TestCase):
    def setUp(self) -> None:
        self.network = Network.from_object(default_network_config)
        return super().setUp()

    def test_json(self):
        """Test json method returns valid json"""
        network_json = self.network.json()
        self.assertIsInstance(network_json, dict)

    def test_get_network_chain_stats(self):
        """Test get network chain stats return valid data"""
        chain_stats = self.network.get_chain_stats()
        self.assertIsInstance(chain_stats, dict)
