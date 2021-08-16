import os
from unittest import TestCase
from unittest.mock import MagicMock

from zerochain.utils import from_json

from tests.utils import TEST_DIR
from tests.mock_response import MockResponse


class BaseTest(TestCase):
    def setup_mock_consensus(self, filename=None, data=None, format="path"):
        if not filename and not data:
            raise TypeError("Atleast filename or data object needs to be passed")

        if format == "path":
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/{self.mock_dir}/{filename}")
            )
            mock_response = MagicMock(return_value=res_obj)
            self.client._consensus_from_workers = mock_response

        else:
            mock_response = MagicMock(return_value=data)
            self.client._consensus_from_workers = mock_response

    def setup_mock_request(self, filename=None, data=None, format="path"):
        if not filename and not data:
            raise TypeError("Atleast filename or data object needs to be passed")

        if format == "path":
            data = from_json(
                os.path.join(TEST_DIR, f"__mocks__/{self.mock_dir}/{filename}")
            )
            response = MockResponse(200, data)
            mock_response = MagicMock(return_value=response)
            self.client._request = mock_response

        else:
            response = MockResponse(200, data)
            mock_response = MagicMock(return_value=response)
            self.client._request = mock_response

    def setup_mock_transaction(self, filename=None, data=None, format="path"):
        if not filename and not data:
            raise TypeError("Atleast filename or data object needs to be passed")

        if format == "path":
            res_obj = from_json(
                os.path.join(TEST_DIR, f"__mocks__/{self.mock_dir}/{filename}")
            )
            mock_response = MagicMock(return_value=res_obj)
            self.client._handle_transaction = mock_response

        else:
            mock_response = MagicMock(return_value=data)
            self.client._handle_transaction = mock_response
