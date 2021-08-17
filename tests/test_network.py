import os
from zerochain.utils import from_json
from zerochain.client import Client
from tests.base_test import BaseTest
from tests.utils import build_client, create_mock_response, TEST_DIR

from zerochain.actions import network

ALLOCATION_ID = "296896621095a9d8a51e6e4dba2bdb5661ea94ffd8fdb0a084301bffd81fe7e6"
BLOBBER_ID = "144a94640cb78130434a79a7a12d0b2c85f819e3ea8856db31c7fde30c30a820"
SHARDER_ID = "0438fa94e4ba923e857375bdce2ceec9ad3200d6ad70e5cf6bdf3a5e21660ab9"


class TestNetwork(BaseTest):
    def setUp(self) -> None:
        self.client = build_client()
        self.mock_dir = "network"
        return super().setUp()

    def test_list_miners(self):
        """Test can list miners"""
        self.setup_mock_consensus(filename="list_miners.json")
        data = network.list_miners(self.client)
        self.assertIsInstance(data, list)

    def test_get_miner_config(self):
        """Test can miner config"""
        self.setup_mock_consensus(filename="miner_config.json")
        data = network.get_miner_config(self.client)
        self.assertIn("view_change", data)

    def test_get_node_stats(self):
        """Test can get node stats"""
        self.setup_mock_consensus(filename="node_stats.json")
        data = network.get_node_stats(self.client, BLOBBER_ID)
        self.assertIn("simple_miner", data)

    def test_list_sharders(self):
        """Test can list sharders"""
        self.setup_mock_consensus(filename="valid_get_latest_magic_block.json")
        data = network.list_sharders(self.client)
        self.assertIn(SHARDER_ID, data)

    def test_get_chain_stats(self):
        """Test can get chain stats"""
        self.setup_mock_consensus(filename="chain_stats.json")
        data = network.get_chain_stats(self.client)
        self.assertIn("block_size", data)

    def test_get_block_by_hash(self):
        """Test can get block by hash"""
        self.setup_mock_consensus(filename="block.json")
        data = network.get_block_by_hash(self.client, "hash")
        self.assertIn("header", data)

    def test_get_block_by_round(self):
        """Test can get block by round number"""
        self.setup_mock_consensus(filename="block.json")
        data = network.get_block_by_hash(self.client, 1112202)
        self.assertIn("header", data)

    def test_get_latest_finalized_block(self):
        """Test can get latest finilized block"""
        self.setup_mock_consensus(filename="valid_get_latest_block.json")
        data = network.get_latest_finalized_block(self.client)
        self.assertIn("version", data)

    def test_get_latest_finalized_block_summary(self):
        """Test can get latest finilized block summary"""
        self.setup_mock_consensus(filename="valid_get_block_summary.json")
        data = network.get_latest_finalized_magic_block_summary(self.client)
        self.assertIn("version", data)

    def test_check_transaction_status(self):
        """Test can get transaction status"""
        self.setup_mock_consensus(filename="confirmed_transaction.json")
        data = network.check_transaction_status(self.client, "hash")
        self.assertIn("txn", data)

    def test_get_worker_stats(self):
        """Test can get worker stats"""
        self.setup_mock_request(filename="worker_stats.json")
        data = network.get_worker_stats(self.client, "sharders")
        self.assertIsInstance(data, dict)

    def test_get_worker_stats(self):
        """Test can get worker stats"""
        self.setup_mock_request(filename="worker_stats.json")
        data = network.get_worker_stats(self.client, "sharders")
        self.assertIsInstance(data, dict)

    def test_get_worker_id(self):
        """Test can get worker id"""
        self.setup_mock_request(filename="worker_id.json")
        data = network.get_worker_id(self.client, "http://worker.com")
        self.assertIsInstance(data, dict)

    def test_create_wallet(self):
        """Test can create client"""
        network.generate_keys = create_mock_response(path="network/gen_keys.json")
        mock_response = create_mock_response(path="network/create_wallet.json")
        self.client.network._consensus_from_workers = mock_response
        data = network.create_wallet(self.client.network)
        self.assertIsInstance(data, Client)

    def test_restore_wallet(self):
        """Test can restore client"""
        network.generate_keys = create_mock_response(path="network/gen_keys.json")
        mock_response = create_mock_response(path="network/create_wallet.json")
        self.client.network._consensus_from_workers = mock_response
        data = network.restore_wallet("some words", self.client.network)
        self.assertIsInstance(data, Client)

    def test_register_wallet(self):
        """Test can register client"""
        mock_response = create_mock_response(path="network/create_wallet.json")
        self.client.network._consensus_from_workers = mock_response
        keys = from_json(os.path.join(TEST_DIR, f"__mocks__/network/gen_keys.json"))
        data = network.register_wallet(keys, self.client.network)
        self.assertIn("id", data)
