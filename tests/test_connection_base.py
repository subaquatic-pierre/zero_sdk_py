from unittest.case import TestCase
from zero_sdk.connection_base import ConnectionBase
from tests.mock_response import MockResponse


class TextConnectionBase(TestCase):
    def setUp(self) -> None:
        self.connection = ConnectionBase()
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
