from tests.base_test import BaseTest
from tests.utils import build_client

from zerochain.actions import blobber

ALLOCATION_ID = "296896621095a9d8a51e6e4dba2bdb5661ea94ffd8fdb0a084301bffd81fe7e6"
BLOBBER_ID = "144a94640cb78130434a79a7a12d0b2c85f819e3ea8856db31c7fde30c30a820"
BLOBBER_URL = "http://beta.0chain.net:31301"


class TestBlobber(BaseTest):
    def setUp(self) -> None:
        self.client = build_client()
        self.mock_dir = "blobber"
        return super().setUp()

    def test_get_blobber_info(self):
        """Test can blobber info"""
        self.setup_mock_consensus(filename="list_blobbers.json")
        data = blobber.get_blobber_info(self.client, BLOBBER_ID)
        self.assertIn("id", data)

    def test_get_blobber_stats(self):
        """Test can blobber stats"""
        self.setup_mock_request(filename="blobber_stats.json")
        data = blobber.get_blobber_stats(self.client, BLOBBER_URL)
        self.assertIn("allocated_size", data)

    def test_list_blobbbers(self):
        """Test can list blobbers"""
        self.setup_mock_consensus(filename="list_blobbers.json")
        data = blobber.list_blobbers(self.client)
        self.assertIsInstance(data, list)

    def test_list_blobbers_by_allocation_id(self):
        """Test can list blobbers by allocation id"""
        self.setup_mock_consensus(filename="list_blobbers.json")
        data = blobber.list_blobbers_by_allocation_id(self.client, ALLOCATION_ID)
        self.assertIsInstance(data, list)

    # TO CONFIRM -----------

    def test_blobber_lock_token(self):
        """Test can lock tokens to blobber"""
        self.setup_mock_transaction(filename="confirmed_transaction.json")
        data = blobber.blobber_lock_token(self.client, 1, BLOBBER_ID)
        self.assertIn("txn", data)

    def test_blobber_unlock_token(self):
        """Test can unlock tokens to blobber"""
        self.setup_mock_transaction(filename="confirmed_transaction.json")
        data = blobber.blobber_unlock_token(self.client, "pool_id", "blobber_id")
        self.assertIn("txn", data)

    def test_update_blobber_settings(self):
        """Test can updateblobber settings"""
        self.setup_mock_consensus("list_blobbers.json")
        self.setup_mock_transaction(filename="unconfirmed_transaction.json")
        data = blobber.update_blobber_settings(self.client, BLOBBER_ID, settings={})
        self.assertIn("async", data)
