import os
from unittest import TestCase
from unittest.mock import MagicMock

from tests.base_test import BaseTest
from tests.utils import TEST_DIR, build_client
from tests.mock_response import MockResponse
from tests.mock_client import MockClient

from zerochain.actions import allocation
from zerochain.allocation import Allocation
from zerochain.utils import from_json

ALLOCATION_ID = "296896621095a9d8a51e6e4dba2bdb5661ea94ffd8fdb0a084301bffd81fe7e6"
BLOBBER_ID = "144a94640cb78130434a79a7a12d0b2c85f819e3ea8856db31c7fde30c30a820"


class TestAllocation(BaseTest):
    def setUp(self) -> None:
        self.client = build_client()
        self.mock_dir = "allocation"
        return super().setUp()

    def test_get_sc_config(self):
        """Test can get strorage contract config"""
        self.setup_mock_consensus(filename="sc_config.json")
        data = allocation.get_sc_config(self.client)
        self.assertIn("time_unit", data)

    def test_create_read_pool(self):
        """Test can create read pool"""
        self.setup_mock_transaction(filename="unconfirmed_transaction.json")
        data = allocation.create_read_pool(self.client)
        self.assertIn("async", data)

    def test_list_read_pool_info(self):
        """Test can get read pool info"""
        self.setup_mock_consensus(filename="pool_info.json")
        data = allocation.list_read_pool_info(self.client)
        self.assertIsInstance(data, list)

    def test_list_read_pool_info_by_allocation_id(self):
        """Test can get read pool info by allocation ID"""
        self.setup_mock_consensus(filename="pool_info.json")
        data = allocation.list_read_pool_by_allocation_id(self.client, ALLOCATION_ID)
        self.assertIsInstance(data, list)

    def test_list_write_pool_info(self):
        """Test can get write pool info"""
        self.setup_mock_consensus(filename="pool_info.json")
        data = allocation.list_read_pool_info(self.client)
        self.assertIsInstance(data, list)

    def test_list_write_pool_by_allocation_id(self):
        """Test can get write pool info by allocation ID"""
        self.setup_mock_consensus(filename="pool_info.json")
        data = allocation.list_read_pool_by_allocation_id(self.client, ALLOCATION_ID)
        self.assertIsInstance(data, list)

    def test_read_pool_lock(self):
        """Test can lock read pool token"""
        self.setup_mock_transaction(data={"status": "locked"}, format="obj")
        data = allocation.read_pool_lock(
            self.client,
            1,
            "allocation_id",
            days=4,
            hours=0,
            minutes=0,
            seconds=0,
            blobber_id=BLOBBER_ID,
        )
        self.assertIn("status", data)

    def test_read_pool_unlock(self):
        """Test can unlock read pool token"""
        self.setup_mock_transaction(data={"status": "un_locked"}, format="obj")
        data = allocation.read_pool_unlock(self.client, "pool_id")
        self.assertIn("status", data)

    def test_write_pool_lock(self):
        """Test can lock write pool token"""
        self.setup_mock_transaction(data={"status": "locked"}, format="obj")
        data = allocation.read_pool_lock(
            self.client,
            1,
            "allocation_id",
            days=4,
            hours=0,
            minutes=0,
            seconds=0,
            blobber_id=BLOBBER_ID,
        )
        self.assertIn("status", data)

    def test_write_pool_unlock(self):
        """Test can unlock write pool token"""
        self.setup_mock_transaction(data={"status": "unlocked"}, format="obj")
        data = allocation.read_pool_unlock(self.client, "pool_id")
        self.assertIn("status", data)

    def test_list_allocations(self):
        """Test can list allocations"""
        self.setup_mock_consensus(filename="list_allocations.json")
        data = allocation.list_allocations(self.client)
        self.assertIsInstance(data, list)

    def test_get_allocation_info(self):
        """Test can allocation info"""
        self.setup_mock_consensus(filename="allocation_info.json")
        data = allocation.get_allocation_info(self.client, ALLOCATION_ID)
        self.assertIn("id", data)

    def test_get_allocation(self):
        """Test can get allocation instance"""
        self.setup_mock_consensus(filename="list_allocations.json")
        data = allocation.get_allocation(self.client, ALLOCATION_ID)
        self.assertIsInstance(data, Allocation)

    def test_create_allocation(self):
        """Test create allocation"""
        self.setup_mock_transaction(filename="confirmed_transaction.json")
        data = allocation.create_allocation(
            self.client,
            data_shards=2,
            parity_shards=2,
            size=10000,
            lock_tokens=1,
            preferred_blobbers=None,
            write_price=1,
            read_price=1,
            max_challenge_completion_time=1,
            expiration_date=1,
        )
        self.assertIsInstance(data, Allocation)

    def test_update_allocation(self):
        """Test update allocation"""
        self.setup_mock_transaction(filename="confirmed_transaction.json")
        data = allocation.update_allocation(
            self.client, extend_expiration_hours=10, size=1
        )
        self.assertIn("txn", data)

    def test_allocation_min_lock(self):
        """Test min lock on allocation"""
        self.setup_mock_consensus(filename="confirmed_transaction.json")
        data = allocation.allocation_min_lock(
            self.client,
            data_shards=2,
            parity_shards=2,
            size=10000,
            preferred_blobbers=None,
            write_price=1,
            read_price=1,
            max_challenge_completion_time=1,
            expiration_date=1,
        )
        self.assertIn("txn", data)

    def test_return_pools(self):
        """Can return pools from data"""
        data = {"pools": ["pool1", "pool2"]}
        res = allocation.return_pools(data)
        self.assertIsInstance(res, list)


# class TestAllocationClientMethods(TestCase):
#     def setUp(self) -> None:
#         self.allocation = Allocation(ALLOCATION_ID, build_client())
#         return super().setUp()

#     def _setup_mock(self, response_data, method_name=None):
#         if type(response_data) == dict or type(response_data) == list:
#             res_obj = response_data
#         else:
#             res_obj = from_json(
#                 os.path.join(TEST_DIR, f"__mocks__/allocation/{response_data}")
#             )
#         if method_name:
#             mock_return = getattr(MockClient, "mock_return")
#             mock_client = MockClient
#             setattr(mock_client, method_name, mock_return(res_obj))
#             self.allocation.client = mock_client
#         else:
#             self.allocation._consensus_from_workers = res_obj

#     def test_get_read_pool_info(self):
#         """Test can get read pool info"""
#         self._setup_mock([], method_name="list_read_pool_info")
#         data = self.allocation.get_read_pool_info()
#         self.assertIsInstance(data, list)

#     def test_get_write_pool_info(self):
#         """Test can get write pool info"""
#         self._setup_mock([], method_name="list_write_pool_info")
#         data = self.allocation.get_write_pool_info()
#         self.assertIsInstance(data, list)

#     def test_client_info(self):
#         """Test can get client info"""
#         self._setup_mock(
#             {
#                 "client_id": "some_id",
#                 "public_key": "public_key",
#             }
#         )
#         data = self.allocation.get_client_info()
#         self.assertIn("client_id", data)

#     def test_get_allocation_info(self):
#         """Test can allocation info by id"""
#         self._setup_mock("allocation_info.json", method_name="get_allocation_info")
#         data = self.allocation.get_allocation_info()
#         self.assertIn("id", data)

#     def test_list_blobbers(self):
#         """Test list all blobbers for allocation"""
#         self._setup_mock("list_blobbers.json", "list_blobbers_by_allocation_id")
#         data = self.allocation.list_blobbers()
#         self.assertIsInstance(data, list)

#     def test_get_blobber_info(self):
#         """Test can get blobber info by id"""
#         self._setup_mock("blobber_info.json", "get_blobber_info")
#         data = self.allocation.get_blobber_info(blobber_id=BLOBBER_ID)
#         self.assertIn("id", data)

#     def test_get_blobber_stats(self):
#         """Test can get blobber stats by url"""
#         self._setup_mock("blobber_stats.json", "get_blobber_stats")
#         data = self.allocation.get_blobber_stats(blobber_url="some")
#         self.assertIn("allocated_size", data)

#     def test_read_pool_lock(self):
#         """Test can lock tokens to read pool"""
#         self._setup_mock({"status": "tokens locked"}, "read_pool_lock")
#         data = self.allocation.read_pool_lock(
#             1,
#         )
#         self.assertIn("status", data)


# class TestAllocationBlobberInfo(TestCase):
#     def setUp(self) -> None:
#         self.allocation = Allocation(ALLOCATION_ID, build_client())
#         return super().setUp()

#     def _setup_mock(self, response_data, is_mock_request=False):
#         if type(response_data) == dict:
#             res_obj = response_data
#         else:
#             res_obj = from_json(
#                 os.path.join(TEST_DIR, f"__mocks__/allocation/{response_data}")
#             )

#         if is_mock_request:
#             response = MockResponse(200, res_obj)
#             request_mock = MagicMock(return_value=response)
#             self.allocation._request = request_mock
#         else:
#             request_mock = MagicMock(return_value=res_obj)
#             self.allocation._consensus_from_workers = request_mock

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
