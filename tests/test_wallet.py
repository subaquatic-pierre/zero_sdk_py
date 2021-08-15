import os
from unittest.case import TestCase
from unittest.mock import MagicMock

from zerochain.wallet import Wallet
from zerochain.wallet import Wallet
from zerochain.utils import from_json, hash_string
from zerochain.exceptions import ConsensusError
from zerochain.allocation import Allocation

from tests.utils import TEST_DIR, build_network, build_wallet
from tests.mock_response import MockResponse

default_wallet_config = from_json(
    os.path.join(TEST_DIR, "__mocks__/wallet/default_wallet.json")
)


class TestWallet(TestCase):
    def setUp(self) -> None:
        self.wallet = build_wallet()
        return super().setUp()

    def _setup_mock(self, response_data):
        if type(response_data) == dict:
            res_obj = response_data
        else:
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/wallet/{response_data}")
            )
        request_mock = MagicMock(return_value=res_obj)
        self.wallet.network._consensus_from_workers = request_mock

    # def test_sign(self):
    #     """Wallet can sign"""
    #     hash = hash_string("this string needs to be hashed")
    #     data = self.wallet.sign(hash)
    #     print(data)
    #     self.assertEqual(len(data), 64)


class TestWalletMethods(TestCase):
    def setUp(self) -> None:
        self.wallet = build_wallet()
        return super().setUp()

    def _setup_mock(self, response_data):
        if type(response_data) == dict:
            res_obj = response_data
        else:
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/wallet/{response_data}")
            )
        request_mock = MagicMock(return_value=res_obj)
        self.wallet._consensus_from_workers = request_mock

    def test_get_balance(self):
        """Test Balance is integer"""
        self._setup_mock("balance.json")
        data = self.wallet.get_balance()
        self.assertIsInstance(data, int)

    def test_get_balance_human(self):
        """Test Balance is human readable"""
        self._setup_mock("balance.json")
        data = self.wallet.get_balance("human")
        self.assertIsInstance(data, str)

    def test_list_read_pool_info(self):
        """Test can get read pool info"""
        self._setup_mock("pool_info.json")
        pool = self.wallet.list_read_pool_info()
        self.assertIsInstance(pool, list)

    def test_list_write_pool_info(self):
        """Test get write pool info"""
        self._setup_mock("pool_info.json")
        pool = self.wallet.list_write_pool_info()
        self.assertIsInstance(pool, list)

    def test_list_stake_pool_info(self):
        """Test list_stake_pool_info"""
        self._setup_mock({"pools": {}})
        data = self.wallet.list_stake_pool_info()
        self.assertIsInstance(data, dict)

    def test_get_stake_pool_info(self):
        """Test get_stake_pool_info"""
        self._setup_mock("worker_id.json")
        data = self.wallet.get_stake_pool_info("node_id", "blobber_id")
        self.assertIsInstance(data, dict)

    def test_get_lock_config(self):
        """Test get_lock_config"""
        self._setup_mock("lock_config.json")
        data = self.wallet.list_lock_token()
        self.assertIn("simple_global_node", data)

    def test_list_lock_pool_info(self):
        """Test list_lock_token"""
        self._setup_mock("pools.json")
        data = self.wallet.list_lock_token()
        self.assertIn("stats", data)

    def test_storage_contract_config(self):
        """Test get_sc_config"""
        self._setup_mock("sc_config.json")
        data = self.wallet.get_sc_config()
        self.assertIn("time_unit", data)


class TestWalletTokenLock(TestCase):
    def setUp(self) -> None:
        self.wallet = build_wallet()
        return super().setUp()

    def _setup_mock(self, response_data):
        if type(response_data) == dict:
            res_obj = response_data
        else:
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/wallet/{response_data}")
            )
        request_mock = MagicMock(return_value=res_obj)
        self.wallet._handle_transaction = request_mock

    def test_lock_token(self):
        """Test get_lock_config"""
        self._setup_mock("smart_contract_confirmation.json")
        data = self.wallet.lock_token(3, 3)
        self.assertIn("hash", data)

    def test_unlock_token(self):
        """Test unlock_token"""
        self._setup_mock("smart_contract_confirmation.json")
        data = self.wallet.lock_token("pool_id")
        self.assertIn("hash", data)

    def test_create_read_pool(self):
        """Test create read pool for wallet"""
        self._setup_mock("create_read_pool.json")
        pool = self.wallet.create_read_pool()
        self.assertIn("entity", pool)

    def test_send_token(self):
        """Test can send token to wallet"""
        self._setup_mock("send_token.json")
        data = self.wallet.send_token("somewalletid", 1, "Test send token")
        self.assertIn("hash", data)


class TestWalletVestingPoolRequest(TestCase):
    def setUp(self) -> None:
        self.wallet = build_wallet()
        return super().setUp()

    def _setup_mock(self, response_data):
        if type(response_data) == dict:
            res_obj = response_data
        else:
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/wallet/{response_data}")
            )
        request_mock = MagicMock(return_value=res_obj)
        self.wallet._handle_transaction = request_mock


class TestWalletVestingPoolRequest(TestCase):
    def setUp(self) -> None:
        self.wallet = build_wallet()
        return super().setUp()

    def _setup_mock(self, response_data):
        if type(response_data) == dict:
            res_obj = response_data
        else:
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/wallet/{response_data}")
            )
        request_mock = MagicMock(return_value=res_obj)
        self.wallet._consensus_from_workers = request_mock

    def test_get_vp_config(self):
        """Test get_vesting_pool_config"""
        self._setup_mock("vp_config.json")
        data = self.wallet.get_vesting_pool_config()
        self.assertIn("min_lock", data)


class TestWalletAllocationTransaction(TestCase):
    def setUp(self) -> None:
        self.wallet = build_wallet()
        return super().setUp()

    def _setup_mock(self, response_data):
        res_obj = from_json(os.path.join(TEST_DIR, f"__mocks__/wallet/{response_data}"))
        request_mock = MagicMock(return_value=res_obj)
        self.wallet._handle_transaction = request_mock

    def test_create_allocation(self):
        """Can create storage allocation"""
        self._setup_mock("smart_contract_confirmation.json")
        data = self.wallet.create_allocation()
        self.assertIsInstance(data, Allocation)

    def test_unlock_read_pool_token(self):
        """Can unlock read pool tockens"""
        self._setup_mock("smart_contract_confirmation.json")
        data = self.wallet.read_pool_unlock("pool_id")
        self.assertIn("hash", data)

    def test_lock_read_pool_token(self):
        """Can unlock read pool tockens"""
        self._setup_mock("smart_contract_confirmation.json")
        data = self.wallet.read_pool_lock(1, "allocation_id", days=1)
        self.assertIn("hash", data)

    # def test_blobber_lock_tokens(self):
    #     """Test can lock tokens to blobber"""
    #     self._setup_mock("lock_token.json")
    #     res = self.wallet.blobber_lock_token(1, "blobber_id")
    #     self.assertIsInstance(res, dict)

    # def test_blobber_unlock_tokens(self):
    #     """Test can unlock tokens from blobber"""
    #     self._setup_mock("lock_token.json")
    #     res = self.wallet.blobber_unlock_token("pool_id", "blobber_id")
    #     self.assertIsInstance(res, dict)


class TestWalletAllocationConsensus(TestCase):
    def setUp(self) -> None:
        self.wallet = build_wallet()
        return super().setUp()

    def _setup_mock(self, response_data):
        if type(response_data) == dict:
            res_obj = response_data
        else:
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/wallet/{response_data}")
            )
        request_mock = MagicMock(return_value=res_obj)
        self.wallet._consensus_from_workers = request_mock

    def test_get_allocation(self):
        """Get allocation returns new instance of alloction"""
        self._setup_mock("list_allocations.json")
        data = self.wallet.get_allocation(
            "296896621095a9d8a51e6e4dba2bdb5661ea94ffd8fdb0a084301bffd81fe7e6"
        )
        self.assertIsInstance(data, Allocation)

    def test_list_allocations(self):
        """Test can list all allocations assigned to wallet"""
        self._setup_mock("list_allocations.json")
        data = self.wallet.list_allocations()
        self.assertIsInstance(data, list)

    def test_get_allocation_info(self):
        """Test can get allocation info by id"""
        self._setup_mock("list_allocations.json")
        data = self.wallet.get_allocation_info(
            "296896621095a9d8a51e6e4dba2bdb5661ea94ffd8fdb0a084301bffd81fe7e6"
        )
        self.assertIn("blobbers", data)
