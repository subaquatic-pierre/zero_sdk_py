from pathlib import Path
from unittest.case import TestCase

from zerochain.utils import (
    from_yaml,
    from_json,
    get_home_path,
    hash_string,
    hostname_from_config_obj,
    verify_data,
)

HOME_DIR = f"{Path.home()}"
DEFAULT_NETWORK = "https://beta.0chain.net"


class TestUtils(TestCase):
    def test_home_path(self):
        """Test get_home_path method returning correct home path"""
        res = get_home_path()
        self.assertTrue(res == HOME_DIR)

    def test_hash_string(self):
        """Test hash_string method returning correct hash string length"""
        message = "this is a super secret message"
        res = hash_string(message)
        self.assertTrue(len(res) == 64)

    def test_from_yaml(self):
        """Test from_yaml returning correct config object"""
        network_config = from_yaml(f"{HOME_DIR}/.zcn/config.yaml")
        self.assertTrue(network_config["block_worker"] is not None)

    def test_hostname_from_config_obj(self):
        """Test hostname_from_config_obj returning correct url"""
        network_config = {"block_worker": "https://beta.0chain.net/dns"}
        url = hostname_from_config_obj(network_config)
        self.assertTrue(url == DEFAULT_NETWORK)

    def test_from_json(self):
        """Test from_json returining correct wallet config"""
        wallet_config = from_json(f"{HOME_DIR}/.zcn/wallet.json")
        self.assertTrue(wallet_config["client_id"] is not None)

    def test_verify_data(self):
        """Test verify_data not returning correct data object"""
        data = {"key": "value"}
        verified_data = verify_data(data)
        self.assertTrue(verified_data["key"] == "value")
