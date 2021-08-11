import os
import json
from unittest.mock import MagicMock
from unittest.case import TestCase


from tests.utils import TEST_DIR, build_network
from tests.mock_response import MockResponse

from zero_sdk.const import Endpoints
from zero_sdk.utils import from_json
from zero_sdk.connection_base import ConnectionBase


class Connection(ConnectionBase):
    pass


class TextConnectionBase(TestCase):
    def setUp(self) -> None:
        self.connection = Connection()
        return super().setUp()

    def _setup_mock(self, status_code, data):
        self.response = MockResponse(status_code, data)

    def test_check_status_code_dict(self):
        self._setup_mock(200, {"header": "Welcome"})
        valid_res = self.connection._check_status_code(self.response)
        self.assertIsInstance(valid_res, dict)
        self.assertIn("header", valid_res)

    def test_check_status_code_string(self):
        res_text = "This is the response text"
        self._setup_mock(200, res_text)
        valid_res = self.connection._check_status_code(
            self.response, return_type="string"
        )
        self.assertIsInstance(valid_res, str)
        self.assertIs(valid_res, res_text)

    def test_check_status_code_string(self):
        res_text = "This is the response text"
        self._setup_mock(200, res_text)
        valid_res = self.connection._check_status_code(self.response)
        self.assertIsInstance(valid_res, str)
        self.assertIs(valid_res, res_text)

    def test_check_status_code_invalid_json(self):
        self._setup_mock(200, None)
        with self.assertRaises(ConnectionError):
            self.connection._check_status_code(
                self.response,
                "There was en error",
                raise_exception=True,
                return_type="json",
            )

    def test_status_code_400_raises_error(self):
        self._setup_mock(400, None)
        with self.assertRaises(ConnectionError):
            self.connection._check_status_code(
                self.response,
                "There was en error",
                raise_exception=True,
                return_type="string",
            )

    def test_status_code_400_return_text(self):
        error_message = "There was en error"
        response_text = "Response Text"
        self._setup_mock(400, response_text)
        valid_response = self.connection._check_status_code(
            self.response,
            error_message,
            return_type="json",
        )
        self.assertIsInstance(valid_response, str)


def get_chain_stats():
    return from_json(
        os.path.join(TEST_DIR, "fixtures/network/valid_chain_stats_response.json")
    )


class TestGetConsensus(TestCase):
    def setUp(self) -> None:
        self.connection = build_network(50)
        return super().setUp()

    def _setup_mock(self, status_code, data):
        response = MockResponse(status_code, data)
        mock_response = MagicMock(return_value=response)
        self.connection._request = mock_response

    def test_successful_response(self):
        self._setup_mock(200, get_chain_stats())
        final_data = self.connection._consensus_from_workers(
            "sharders", "http://placeholder.com"
        )
        self.assertIn("current_round", final_data)

    def test_min_consensus_error(self):
        self.connection = build_network(200)
        self._setup_mock(200, get_chain_stats())
        with self.assertRaises(Exception):
            self.connection._consensus_from_workers(
                "sharders", "http://placeholder.com"
            )

    def test_error_balance_wallet(self):
        self._setup_mock(200, json.dumps({"error": "value not present"}))
        empty_return_value = {"balance": 0}
        data = self.connection._consensus_from_workers(
            "sharders", Endpoints.GET_BALANCE, empty_return_value=empty_return_value
        )
        self.assertIn("balance", data)

    # TODO - TESTS
    def test_handle_empty_return_value(self):
        pass
