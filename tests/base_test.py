import os
from unittest import TestCase
from unittest.mock import MagicMock

from zerochain.utils import from_json

from tests.utils import TEST_DIR, build_client
from tests.mock_response import MockResponse


class BaseTest(TestCase):
    def __init__(self, path) -> None:
        self.client = build_client()
        self.mock_path = path
        super().__init__()

    def setup_mock_consensus_from_path(self, filename):
        res_obj = from_json(
            os.path.join(TEST_DIR, f"__mocks__/{self.mock_path}/{filename}")
        )
        mock_response = MagicMock(return_value=res_obj)
        self.client._consensus_from_workers = mock_response

    def setup_mock_consensus_from_obj(self, obj):
        mock_response = MagicMock(return_value=obj)
        self.client._consensus_from_workers = mock_response

    def setup_mock_request_from_path(self, filename):
        data = from_json(
            os.path.join(TEST_DIR, f"__mocks__/{self.mock_path}/{filename}")
        )
        response = MockResponse(200, data)
        mock_response = MagicMock(return_value=response)
        self.client._request = mock_response

    def setup_mock_request_from_obj(self, obj):
        response = MockResponse(200, obj)
        mock_response = MagicMock(return_value=response)
        self.client._request = mock_response
