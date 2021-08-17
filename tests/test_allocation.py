from tests.base_test import BaseTest
from tests.utils import build_client

from zerochain.actions import allocation
from zerochain.allocation import Allocation

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
        data = allocation.list_read_pool_info(self.client, ALLOCATION_ID)
        self.assertIsInstance(data, list)

    def test_list_write_pool_info(self):
        """Test can get write pool info"""
        self.setup_mock_consensus(filename="pool_info.json")
        data = allocation.list_read_pool_info(self.client)
        self.assertIsInstance(data, list)

    def test_list_write_pool_by_allocation_id(self):
        """Test can get write pool info by allocation ID"""
        self.setup_mock_consensus(filename="pool_info.json")
        data = allocation.list_write_pool_info(self.client, ALLOCATION_ID)
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
            self.client,
            "allocation_id",
            extend_expiration_hours=10,
            size=1,
            set_immutable=False,
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
