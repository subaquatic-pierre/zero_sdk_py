from unittest import TestCase
from zero_sdk.allocation import Allocation
from zero_sdk.wallet import Wallet
from zero_sdk.config import config


class AllocationTest(TestCase):
    def setUp(self) -> None:
        self.wallet = Wallet()
        self.main_alloc = Allocation(config.MAIN_ALLOCATION_ID, self.wallet)
        return super().setUp()

    def test_has_id(self):
        """Allocation does not have an ID"""
        self.assertTrue(hasattr(self.main_alloc, "id"))

    def test_has_wallet(self):
        """Wallet was not assigned to allocation"""
        self.assertTrue(hasattr(self.main_alloc, "wallet"))
