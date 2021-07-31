from unittest.case import TestCase
from zero_sdk.wallet import Wallet
import pytest


class TestWallet(TestCase):
    def test_wallet_init_exception(self):
        """Test Error raised on incorrect wallet config"""
        with self.assertRaises(Exception):
            error_wallet = Wallet(default_config=False)
            self.assertTrue(
                str(error_wallet.value)
                == "If default config not selected a config object needs to passed to constructor"
            )

    def test_wallet_config_exception(self):
        """Test Error raised on incorrect wallet config"""
        with self.assertRaises(Exception):
            no_config_wallet = Wallet(default_config=False, config={})
            error = no_config_wallet.get_balance()
            self.assertTrue(
                str(error)
                == "Wallet is not initialized, call 'create_wallet, init_wallet or recover_wallet' methods to configure wallet"
            )

    def test_get_balance(self):
        """Test Balance is integer"""
        wallet = Wallet()
        balance = wallet.get_balance()
        self.assertTrue(isinstance(balance, int))

    def test_add_tokens(self):
        """Test add_token method did not add to wallet balance"""
        wallet = Wallet()
        self.assertTrue(wallet.add_tokens())
