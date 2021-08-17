from tests.base_test import BaseTest
from tests.utils import build_client

from zerochain.actions import wallet
from zerochain.allocation import Allocation

ALLOCATION_ID = "296896621095a9d8a51e6e4dba2bdb5661ea94ffd8fdb0a084301bffd81fe7e6"
BLOBBER_ID = "144a94640cb78130434a79a7a12d0b2c85f819e3ea8856db31c7fde30c30a820"


class TestAllocation(BaseTest):
    def setUp(self) -> None:
        self.client = build_client()
        self.mock_dir = "allocation"
        return super().setUp()

    def test_get_balance(self):
        """Test can get wallet balance"""
        self.setup_mock_consensus(data=10, format="number")
        data = wallet.get_balance(self.client)
        self.assertIsInstance(data, int)

    def test_send_token(self):
        """Test can send token"""
        self.setup_mock_transaction("confirmed_transaction.json")
        data = wallet.send_token(
            self.client, "to_client", 10, description="Cool money send"
        )
        self.assertIn("txn", data)
