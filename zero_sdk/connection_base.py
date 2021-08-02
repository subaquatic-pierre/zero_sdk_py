from requests import request
from requests.models import Response


class ConnectionBase:
    def _validate_response(
        self,
        res,
        error_message="",
        raise_exception=False,
        return_type="json",
    ) -> dict or str:
        """Validate network response
        Check network response status on each request
        Return error message if status code is not 200
        :param res: Response object
        :param error_message: String message to display on error
        :param raise_exception: Bool, raise an execption on error
        :param return_type: String, expected return type
        """
        if res.status_code == 200:
            try:
                # successfull code 200 response with valid json
                if return_type == "json":
                    return res.json()
                if return_type == "string":
                    return res.text
            except:
                # unable to parse response
                if raise_exception:
                    raise ConnectionError(f"{error_message} - Message: {res.text}")
                else:
                    return f"{error_message} - Message: {res.text}"
        else:
            if raise_exception:
                raise ConnectionError(f"{error_message} - Message: {res.text}")
            else:
                return f"{error_message} - Message: {res.text}"

    def _request(self, method, url, headers=None, data=None, files=None) -> Response:
        """Base request method for model requests
        Returns valid res data as json string
        :param method: String
        :param url: String
        :param headers: Dict, headers keys and values
        :param data: Dict
        :param files: Tuple or List
        :param error_message: String, message to display if error
        """
        res = request(method, url, headers=headers, data=data, files=files)
        return res
