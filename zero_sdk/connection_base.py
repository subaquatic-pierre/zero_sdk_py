class ConnectionBase:
    def _validate_response(self, res, error_message) -> object:
        """Validate network response
        Check network response status on each request
        Return error message if status code is not 200
        """
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception(f"{error_message} - Message: {res.text}")
