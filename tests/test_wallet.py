import os
from unittest.case import TestCase
from unittest.mock import MagicMock

from zero_sdk.wallet import Wallet
from zero_sdk.wallet import Wallet
from zero_sdk.utils import from_json
from zero_sdk.exceptions import ConsensusError

from tests.utils import TEST_DIR, build_network, build_wallet
from tests.mock_response import MockResponse

default_wallet_config = from_json(
    os.path.join(TEST_DIR, "fixtures/default_wallet.json")
)


class TestWalletInit(TestCase):
    def setUp(self) -> None:
        self.network = build_network(50)
        return super().setUp()

    def test_from_object(self):
        """Test network can be instantiated from standard config object"""
        wallet = Wallet.from_object(default_wallet_config, self.network)
        self.assertTrue(wallet)

    def test_error_from_object(self):
        """Test an error is thrown on incorrect config object sent to from object method"""
        with self.assertRaises(Exception):
            wallet = Wallet.from_object({})
            self.assertTrue(wallet)


class TestWalletMethods(TestCase):
    def setUp(self) -> None:
        self.wallet = build_wallet()
        return super().setUp()

    def _setup_mock(self, data):
        mock_response = MockResponse(200, data)
        request_mock = MagicMock(return_value=mock_response)
        self.wallet._request = request_mock

    def test_get_balance(self):
        """Test Balance is integer"""
        self._setup_mock({"balance": 20000})
        balance = self.wallet.get_balance()
        self.assertIn("balance", balance)

    def test_get_locked_tokens(self):
        """Test Balance is integer"""
        self._setup_mock({"locked_tokens": []})
        locked_tockens = self.wallet.get_locked_tokens()
        self.assertIn("locked_tokens", locked_tockens)

    # def test_add_tokens(self):
    #     """Test add_token method add to wallet balance"""
    #     wallet = Wallet()
    #     self.assertTrue(wallet.add_tokens())
