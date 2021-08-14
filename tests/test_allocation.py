import os
from unittest import TestCase
from unittest.mock import MagicMock

from tests.utils import TEST_DIR, build_wallet
from tests.mock_response import MockResponse

from zerochain.allocation import Allocation
from zerochain.utils import from_json

ALLOCATION_ID = "296896621095a9d8a51e6e4dba2bdb5661ea94ffd8fdb0a084301bffd81fe7e6"


class AllocationTestConsensus(TestCase):
    def setUp(self) -> None:
        self.allocation = Allocation(ALLOCATION_ID, build_wallet())
        return super().setUp()

    def _setup_mock(self, response_data):
        if type(response_data) == dict:
            res_obj = response_data
        else:
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/allocation/{response_data}")
            )
        request_mock = MagicMock(return_value=res_obj)
        self.allocation._consensus_from_workers = request_mock

    def test_get_allocation_info(self):
        """Test can get allocation info"""
        self._setup_mock("allocation_info.json")
        data = self.allocation.get_allocation_info()
        self.assertIn("id", data)


class AllocationTestBlobberInfo(TestCase):
    def setUp(self) -> None:
        self.allocation = Allocation(ALLOCATION_ID, build_wallet())
        return super().setUp()

    def _setup_mock(self, response_data, is_mock_request=False):
        if type(response_data) == dict:
            res_obj = response_data
        else:
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/allocation/{response_data}")
            )

        if is_mock_request:
            response = MockResponse(200, res_obj)
            request_mock = MagicMock(return_value=response)
            self.allocation._request = request_mock
        else:
            request_mock = MagicMock(return_value=res_obj)
            self.allocation._consensus_from_workers = request_mock

    def test_list_blobbers(self):
        """Test list all blobbers for allocation"""
        self._setup_mock("list_blobbers.json")
        data = self.allocation.list_blobbers()
        self.assertIsInstance(data, list)

    def test_get_blobber_info(self):
        """Test can get blobber info by id"""
        self._setup_mock("list_blobbers.json")
        data = self.allocation.get_blobber_info(
            blobber_id="144a94640cb78130434a79a7a12d0b2c85f819e3ea8856db31c7fde30c30a820"
        )
        self.assertIn("id", data)

    def test_get_blobber_stats(self):
        """Test can get blobber stats by url"""
        self._setup_mock("blobber_stats.json", is_mock_request=True)
        data = self.allocation.get_blobber_stats(blobber_url="some")
        self.assertIn("allocated_size", data)

    # def test_get_all_blobber_stats(self):
    #     """Test can stats for all blobbers"""
    #     self._setup_mock("all_blobber_stats.json")
    #     res = self.allocation.get_blobber_stats()
    #     self.assertIsInstance(res, list)

    # def test_get_all_blobber_stats(self):
    #     """Test can stats for single blobber"""
    #     self._setup_mock("blobber_stats.json")
    #     res = self.allocation.get_blobber_stats("http://beta.0chain.net:31301")
    #     self.assertIn("allocated_size", res)
