from requests import request
from requests.api import head


class ConnectionBase:
    def _validate_response(self, res, error_message="") -> object:
        """Validate network response
        Check network response status on each request
        Return error message if status code is not 200
        :param res: Response object
        :param error_message: String message to display on error
        """
        if res.status_code == 200:
            return res.json()
        else:
            return f"{error_message} - Message: {res.text}"

    def _request(
        self, method, url, headers=None, data=None, files=None, error_message=None
    ):
        """Base request method for model requests
        Returns valid res data as json string
        :param method: String
        :param url: String
        :param headers: Dict, headers keys and values
        :param data: Dict
        :param files: Tuple | List
        :param error_message: String, message to display if error
        """
        res = request(method, url, headers=headers, data=data, files=files)
        valid_res = self._validate_response(res, error_message)
        return valid_res
