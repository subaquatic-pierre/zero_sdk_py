import os
from unittest import TestCase
from unittest.mock import MagicMock

from tests.utils import TEST_DIR, build_wallet
from tests.mock_response import MockResponse
from tests.mock_wallet import MockWallet

from zerochain.allocation import Allocation
from zerochain.utils import from_json

ALLOCATION_ID = "296896621095a9d8a51e6e4dba2bdb5661ea94ffd8fdb0a084301bffd81fe7e6"
BLOBBER_ID = "144a94640cb78130434a79a7a12d0b2c85f819e3ea8856db31c7fde30c30a820"


class TestAllocationWalletMethods(TestCase):
    def setUp(self) -> None:
        self.allocation = Allocation(ALLOCATION_ID, build_wallet())
        return super().setUp()

    def _setup_mock(self, response_data, method_name=None):
        if type(response_data) == dict or type(response_data) == list:
            res_obj = response_data
        else:
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/allocation/{response_data}")
            )
        if method_name:
            mock_return = getattr(MockWallet, "mock_return")
            mock_wallet = MockWallet
            setattr(mock_wallet, method_name, mock_return(res_obj))
            self.allocation.wallet = mock_wallet
        else:
            self.allocation._consensus_from_workers = res_obj

    def test_get_read_pool_info(self):
        """Test can get read pool info"""
        self._setup_mock([], method_name="list_read_pool_info")
        data = self.allocation.get_read_pool_info()
        self.assertIsInstance(data, list)

    def test_get_write_pool_info(self):
        """Test can get write pool info"""
        self._setup_mock([], method_name="list_write_pool_info")
        data = self.allocation.get_write_pool_info()
        self.assertIsInstance(data, list)

    def test_wallet_info(self):
        """Test can get wallet info"""
        self._setup_mock(
            {
                "client_id": "some_id",
                "public_key": "public_key",
            }
        )
        data = self.allocation.get_wallet_info()
        self.assertIn("client_id", data)

    def test_get_allocation_info(self):
        """Test can allocation info by id"""
        self._setup_mock("allocation_info.json", method_name="get_allocation_info")
        data = self.allocation.get_allocation_info()
        self.assertIn("id", data)

    def test_list_blobbers(self):
        """Test list all blobbers for allocation"""
        self._setup_mock("list_blobbers.json", "list_blobbers_by_allocation_id")
        data = self.allocation.list_blobbers()
        self.assertIsInstance(data, list)

    def test_get_blobber_info(self):
        """Test can get blobber info by id"""
        self._setup_mock("blobber_info.json", "get_blobber_info")
        data = self.allocation.get_blobber_info(blobber_id=BLOBBER_ID)
        self.assertIn("id", data)

    def test_get_blobber_stats(self):
        """Test can get blobber stats by url"""
        self._setup_mock("blobber_stats.json", "get_blobber_stats")
        data = self.allocation.get_blobber_stats(blobber_url="some")
        self.assertIn("allocated_size", data)

    def test_read_pool_lock(self):
        """Test can lock tokens to read pool"""
        self._setup_mock({"status": "tokens locked"}, "read_pool_lock")
        data = self.allocation.read_pool_lock(
            1,
        )
        self.assertIn("allocated_size", data)


class TestAllocationBlobberInfo(TestCase):
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
