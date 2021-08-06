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
        self._setup_mock("allocation_info.json")
        info = self.allocation.get_allocation_info()
        self.assertIn("data_shards", info)
