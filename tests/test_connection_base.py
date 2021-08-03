import os
from unittest.mock import MagicMock
from tests.utils import TEST_DIR
from unittest.case import TestCase

from zero_sdk.utils import from_json
from zero_sdk.connection_base import ConnectionBase
from zero_sdk.network import Network
from zero_sdk.workers import Miner, Sharder, Blobber
from tests.mock_response import MockResponse


class Connection(ConnectionBase):
    pass


class TextConnectionBase(TestCase):
    def setUp(self) -> None:
        self.connection = Connection()
        return super().setUp()

    def _setup_mock(self, status_code, data):
        self.response = MockResponse(status_code, data)

    def test_validate_response_dict(self):
        self._setup_mock(200, {"header": "Welcome"})
        valid_res = self.connection._validate_response(self.response)
        self.assertIsInstance(valid_res, dict)
        self.assertIn("header", valid_res)

    def test_validate_response_string(self):
        res_text = "This is the response text"
        self._setup_mock(200, res_text)
        valid_res = self.connection._validate_response(
            self.response, return_type="string"
        )
        self.assertIsInstance(valid_res, str)
        self.assertIs(valid_res, res_text)

    def test_validate_response_string(self):
        res_text = "This is the response text"
        self._setup_mock(200, res_text)
        valid_res = self.connection._validate_response(self.response)
        self.assertIsInstance(valid_res, str)
        self.assertIs(valid_res, res_text)

    def test_validate_response_invalid_json(self):
        self._setup_mock(200, None)
        with self.assertRaises(ConnectionError):
            self.connection._validate_response(
                self.response,
                "There was en error",
                raise_exception=True,
                return_type="json",
            )

    def test_status_code_400_raises_error(self):
        self._setup_mock(400, None)
        with self.assertRaises(ConnectionError):
            self.connection._validate_response(
                self.response,
                "There was en error",
                raise_exception=True,
                return_type="string",
            )

    def test_status_code_400_return_text(self):
        error_message = "There was en error"
        response_text = "Response Text"
        self._setup_mock(400, response_text)
        valid_response = self.connection._validate_response(
            self.response,
            error_message,
            return_type="json",
        )
        self.assertEqual(valid_response, f"{error_message} - Message: {response_text}")


def build_connection(min_confirmations):
    placeholder_workers = [
        "http://worker01.com",
        "http://worker02.com",
        "http://worker03.com",
    ]
    miners = [Miner(url) for url in placeholder_workers]
    sharders = [Sharder(url) for url in placeholder_workers]
    blobbers = [Blobber(url) for url in placeholder_workers]
    return Network(
        "http://placehoder.com", miners, sharders, blobbers, min_confirmations
    )


def get_chain_stats():
    return from_json(os.path.join(TEST_DIR, "fixtures/valid_chain_stats_response.json"))


class TestGetConsensus(TestCase):
    def setUp(self) -> None:
        self.connection = build_connection(50)
        return super().setUp()

    def _setup_mock(self, status_code, data):
        response = MockResponse(status_code, data)
        mock_response = MagicMock(return_value=response)
        self.connection._request = mock_response

    def test_successful_response(self):
        self._setup_mock(200, get_chain_stats())
        final_data = self.connection._get_consensus_from_workers(
            "sharders", "http://placeholder.com"
        )
        self.assertIn("current_round", final_data)

    def test_error_string_response(self):
        self._setup_mock(200, "Error returned from server")
        with self.assertRaises(Exception):
            self.connection._get_consensus_from_workers(
                "sharders", "http://placeholder.com"
            )

    def test_error_key_in_response(self):
        chain_stats_obj = get_chain_stats()
        chain_stats_obj["error"] = "There was an error"
        self._setup_mock(200, chain_stats_obj)
        with self.assertRaises(Exception):
            self.connection._get_consensus_from_workers(
                "sharders", "http://placeholder.com"
            )

    def test_error_status_code_response(self):
        self._setup_mock(400, get_chain_stats())
        with self.assertRaises(Exception):
            self.connection._get_consensus_from_workers(
                "sharders", "http://placeholder.com"
            )

    def test_min_consensus_error(self):
        self.connection = build_connection(200)
        self._setup_mock(200, get_chain_stats())
        with self.assertRaises(Exception):
            self.connection._get_consensus_from_workers(
                "sharders", "http://placeholder.com"
            )
