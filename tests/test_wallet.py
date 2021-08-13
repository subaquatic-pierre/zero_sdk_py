import os
from unittest.case import TestCase
from unittest.mock import MagicMock

from zero_sdk.wallet import Wallet
from zero_sdk.wallet import Wallet
from zero_sdk.utils import from_json
from zero_sdk.exceptions import ConsensusError
from zero_sdk.allocation import Allocation

from tests.utils import TEST_DIR, build_network, build_wallet
from tests.mock_response import MockResponse

default_wallet_config = from_json(
    os.path.join(TEST_DIR, "__mocks__/wallet/default_wallet.json")
)


class TestWalletNetwork(TestCase):
    def setUp(self) -> None:
        self.wallet = build_wallet()
        return super().setUp()

    def _setup_mock(self, filename):
        if type(filename) == dict:
            res_obj = filename
        else:
            res_obj = from_json(os.path.join(TEST_DIR, f"__mocks__/wallet/{filename}"))
        request_mock = MagicMock(return_value=res_obj)
        self.wallet.network._consensus_from_workers = request_mock


class TestWalletMethods(TestCase):
    def setUp(self) -> None:
        self.wallet = build_wallet()
        return super().setUp()

    def _setup_mock(self, filename):
        if type(filename) == dict:
            res_obj = filename
        else:
            res_obj = from_json(os.path.join(TEST_DIR, f"__mocks__/wallet/{filename}"))
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
        self.assertIn("pools", pool)

    def test_list_write_pool_info(self):
        """Test get write pool info"""
        self._setup_mock("pool_info.json")
        pool = self.wallet.list_write_pool_info()
        self.assertIn("pools", pool)

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


class TestWalletTokenLock(TestCase):
    def setUp(self) -> None:
        self.wallet = build_wallet()
        return super().setUp()

    def _setup_mock(self, filename):
        if type(filename) == dict:
            res_obj = filename
        else:
            res_obj = from_json(os.path.join(TEST_DIR, f"__mocks__/wallet/{filename}"))
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

    def _setup_mock(self, filename):
        if type(filename) == dict:
            res_obj = filename
        else:
            res_obj = from_json(os.path.join(TEST_DIR, f"__mocks__/wallet/{filename}"))
        request_mock = MagicMock(return_value=res_obj)
        self.wallet._handle_transaction = request_mock


class TestWalletVestingPoolRequest(TestCase):
    def setUp(self) -> None:
        self.wallet = build_wallet()
        return super().setUp()

    def _setup_mock(self, filename):
        if type(filename) == dict:
            res_obj = filename
        else:
            res_obj = from_json(os.path.join(TEST_DIR, f"__mocks__/wallet/{filename}"))
        request_mock = MagicMock(return_value=res_obj)
        self.wallet._consensus_from_workers = request_mock

    def test_get_vp_config(self):
        """Test get_vesting_pool_config"""
        self._setup_mock("vp_config.json")
        data = self.wallet.get_vesting_pool_config()
        self.assertIn("min_lock", data)

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


# class TestWalletAllocation(TestCase):
#     def setUp(self) -> None:
#         self.wallet = build_wallet()
#         return super().setUp()

#     def _setup_mock(self, filename):
#         res_obj = from_json(os.path.join(TEST_DIR, f"__mocks__/wallet/{filename}"))
#         mock_response = MockResponse(200, res_obj)
#         request_mock = MagicMock(return_value=mock_response)
#         self.wallet._request = request_mock

#     def test_list_allocations(self):
#         """Test can list all allocations assigned to wallet"""
#         self._setup_mock("list_allocations.json")
#         allocations = self.wallet.list_allocations()
#         self.assertIsInstance(allocations, list)

#     def test_create_allocation(self):
#         """Can create storage allocation"""
#         self._setup_mock("create_allocation.json")
#         self.wallet.network.check_transaction_status = MagicMock(
#             return_value={"hash": True}
#         )
#         res = self.wallet.create_allocation()
#         self.assertIsInstance(res, Allocation)
