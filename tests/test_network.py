from unittest.case import TestCase
from unittest.mock import MagicMock
import os
from zero_sdk.wallet import Wallet

from zero_sdk.workers import Blobber, Miner, Sharder
from zero_sdk.network import Network
from zero_sdk.utils import from_yaml, from_json

from tests.utils import TEST_DIR
from tests.mock_response import MockResponse

BLOCK_ID = "ed79cae70d439c11258236da1dfa6fc550f7cc569768304623e8fbd7d70efae4"
ROUND_NUMBER = "832629"


default_network_config = from_yaml(
    os.path.join(TEST_DIR, "__mocks__/network/default_network.yaml")
)


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

    def test_has_min_confirmation(self):
        """Test network has atleast one shrader"""
        min_confirmation = self.network.min_confirmation
        self.assertGreater(min_confirmation, 0)


class TestNetworkChainMethods(TestCase):
    def setUp(self) -> None:
        self.network = Network(
            "url",
            [Miner("url")],
            [Sharder("url")],
            [Blobber("url")],
            min_confirmation=50,
        )
        return super().setUp()

    def _setup_mock(self, response_data):
        res_obj = from_json(
            os.path.join(TEST_DIR, f"__mocks__/network/{response_data}")
        )
        request_mock = MagicMock(return_value=res_obj)
        self.network._consensus_from_workers = request_mock

    def test_get_network_chain_stats(self):
        """Test get_network_chain_stats returns valid data"""
        self._setup_mock("valid_chain_stats_response.json")
        chain_stats = self.network.get_chain_stats()
        self.assertIsInstance(chain_stats, dict)

    def test_get_block_by_hash(self):
        """Test get_block returns valid data"""
        self._setup_mock("valid_get_block_response.json")
        block_info = self.network.get_block_by_hash(BLOCK_ID)
        self.assertIsInstance(block_info, dict)

    def test_get_block_by_round(self):
        """Test get_block returns valid data"""
        self._setup_mock("valid_get_block_response.json")
        block_info = self.network.get_block_by_round(ROUND_NUMBER)
        self.assertIsInstance(block_info, dict)

    def test_get_latest_finalized_block(self):
        """Test get_latest_finalized block returns valid data"""
        self._setup_mock("valid_get_latest_block.json")
        block_info = self.network.get_latest_finalized_block()
        self.assertIsInstance(block_info, dict)

    def test_get_latest_finalized_magic_block(self):
        """Test get_latest_finalized_magic_block returns valid data"""
        self._setup_mock("valid_get_latest_magic_block.json")
        block_info = self.network.get_latest_finalized_magic_block()
        self.assertIsInstance(block_info, dict)

    def test_get_latest_finalized_magic_block_summary(self):
        """Test get_latest_finalized block returns valid data"""
        self._setup_mock("valid_get_block_summary.json")
        block_info = self.network.get_latest_finalized_magic_block_summary()
        self.assertIsInstance(block_info, dict)

    def test_check_transaction(self):
        """Test get_latest_finalized block returns valid data"""
        self._setup_mock("check_txn_response.json")
        block_info = self.network.check_transaction_status("thisistransactionhash")
        self.assertIsInstance(block_info, dict)

    def test_restore_wallet(self):
        """Test get_latest_finalized block returns valid data"""
        self._setup_mock("create.json")
        wallet = self.network.restore_wallet("this is a mnonnic key phrase")
        self.assertIn("id", wallet)

    def test_create_wallet(self):
        """Test get_latest_finalized block returns valid data"""
        self._setup_mock("create.json")
        wallet = self.network.create_wallet()
        self.assertIsInstance(wallet, Wallet)


class TestNetworkMethods(TestCase):
    def setUp(self) -> None:
        self.network = Network(
            "url",
            [Miner("url")],
            [Sharder("url")],
            [Blobber("url")],
            min_confirmation=50,
        )
        return super().setUp()

    def _setup_mock(self, response_data):
        if type(response_data) == dict:
            res_obj = response_data
        else:
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/network/{response_data}")
            )
        request_mock = MagicMock(return_value=res_obj)
        self.network._consensus_from_workers = request_mock

    def test_json(self):
        """Test json method returns valid json"""
        network_json = self.network.json()
        self.assertIsInstance(network_json, dict)

    def test_list_miners(self):
        """Test list all miners"""
        self._setup_mock("miner_list.json")
        data = self.network.list_miners()
        self.assertIsInstance(data, list)

    def test_list_sharders(self):
        """Test list all sharders"""
        self._setup_mock({"magic_block": {"sharders": {"nodes": {"version": "1"}}}})
        data = self.network.list_sharders()
        self.assertIn("version", data)

    def test_get_miner_config(self):
        """Test get miner config"""
        self._setup_mock("miner_config.json")
        data = self.network.get_miner_config()
        self.assertIn("view_change", data)

    def test_get_node_stats(self):
        """Test node stats"""
        self._setup_mock("node_stats.json")
        data = self.network.get_node_stats(node_id="someid")
        self.assertIn("simple_miner", data)


class TestNetworkRequest(TestCase):
    def setUp(self) -> None:
        self.network = Network(
            "url",
            [Miner("url")],
            [Sharder("url")],
            [Blobber("url")],
            min_confirmation=50,
        )
        return super().setUp()

    def _setup_mock(self, response_data):
        if type(response_data) == dict:
            res_obj = response_data
            response = MockResponse(200, res_obj)
        else:
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/network/{response_data}")
            )
            response = MockResponse(200, res_obj)

        request_mock = MagicMock(return_value=response)
        self.network._request = request_mock

    def test_get_worker_id(self):
        """Test get worker id from url"""
        self._setup_mock("worker_id.json")
        data = self.network.get_worker_id("someurl")
        self.assertIsInstance(data, dict)
