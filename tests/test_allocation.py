import os
from unittest import TestCase
from unittest.mock import MagicMock

from tests.utils import TEST_DIR, build_wallet
from tests.mock_response import MockResponse

from zero_sdk.allocation import Allocation
from zero_sdk.utils import from_json

ALLOCATION_ID = "296896621095a9d8a51e6e4dba2bdb5661ea94ffd8fdb0a084301bffd81fe7e6"


class AllocationTest(TestCase):
    def setUp(self) -> None:
        self.allocation = Allocation(ALLOCATION_ID, build_wallet())
        return super().setUp()

    def _setup_mock(self, filename):
        res_obj = from_json(os.path.join(TEST_DIR, f"fixtures/allocation/{filename}"))
        mock_response = MockResponse(200, res_obj)
        request_mock = MagicMock(return_value=mock_response)
        self.allocation._request = request_mock

    def test_get_allocation_info(self):
        """Test can get valid allocation info"""
        self._setup_mock("allocation_info.json")
        info = self.allocation.get_allocation_info()
        self.assertIn("data_shards", info)

    def test_get_all_blobber_stats(self):
        """Test can stats for all blobbers"""
        self._setup_mock("all_blobber_stats.json")
        res = self.allocation.get_blobber_stats()
        self.assertIsInstance(res, list)

    def test_get_all_blobber_stats(self):
        """Test can stats for single blobber"""
        self._setup_mock("blobber_stats.json")
        res = self.allocation.get_blobber_stats("http://beta.0chain.net:31301")
        self.assertIn("allocated_size", res)
