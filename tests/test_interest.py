from tests.base_test import BaseTest
from tests.utils import build_client

from zerochain.actions import interest
from zerochain.allocation import Allocation

ALLOCATION_ID = "296896621095a9d8a51e6e4dba2bdb5661ea94ffd8fdb0a084301bffd81fe7e6"
BLOBBER_ID = "144a94640cb78130434a79a7a12d0b2c85f819e3ea8856db31c7fde30c30a820"


class TestAllocation(BaseTest):
    def setUp(self) -> None:
        self.client = build_client()
        self.mock_dir = "interest"
        return super().setUp()

    def test_list_lock_tocken(self):
        """Test can list lock token"""
        self.setup_mock_consensus(filename="list_lock_token.json")
        data = interest.list_lock_token(self.client)
        self.assertIn("stats", data)

    def test_get_lock_config(self):
        """Test can get lock token config"""
        self.setup_mock_consensus(filename="lock_config.json")
        data = interest.get_lock_config(self.client)
        self.assertIn("ID", data)

    def test_lock_token(self):
        """Test can lock token"""
        self.setup_mock_transaction(filename="confirmed_transaction.json")
        data = interest.lock_token(self.client, 1, hours=1, minutes=2)
        self.assertIn("txn", data)

    def test_unlock_token(self):
        """Test can get lock token config"""
        self.setup_mock_transaction(filename="confirmed_transaction.json")
        data = interest.unlock_token(self.client, "pool_id")
        self.assertIn("txn", data)
