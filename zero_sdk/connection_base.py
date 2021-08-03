from requests import request
import json
from requests.models import Response
from zero_sdk.utils import hash_string


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

    def _get_consensus_from_workers(self, worker, endpoint) -> dict:
        worker_string = worker
        workers = self._get_workers(worker_string)

        # Create map:
        # {
        #   hashed_data_string: {
        #       data: response.json(),
        #       num_confirmations: int
        #    }
        # }
        response_hash_map = {}

        # Loop through workers
        for worker in workers:
            url = f"{worker.url}/{endpoint}"

            res = self._request("GET", url)
            valid_response = self._validate_response(res)

            # May be string response if node is down, ensure valid dict object
            if type(valid_response) == dict:

                # JSON response may contain error, do not add to response map, not valid transaction
                err = valid_response.get("error")
                if err:
                    continue

                # Build response hash string
                response_hash_string = hash_string(json.dumps(valid_response))

                # Check if key exists in response map
                existing_response_key = response_hash_map.get(response_hash_string)

                # Increment consensus count if key exists
                if existing_response_key:
                    prev_count = existing_response_key.get("num_confirmations")
                    response_hash_map[response_hash_string] = {
                        "data": valid_response,
                        "num_confirmations": prev_count + 1,
                    }
                # Add key to response map if does not exists
                else:
                    response_hash_map[response_hash_string] = {
                        "data": valid_response,
                        "num_confirmations": 1,
                    }

        if len(response_hash_map) == 0:
            raise Exception("No consesus reached from workers")

        consensus_data = self._get_consensus_data(response_hash_map, worker_string)
        return consensus_data

    def _get_consensus_data(self, consensus_data, worker):
        min_confirmation = self._get_min_confirmation()
        greatest_num_confirmations = 0
        key_for_highest_confirmations = ""

        # Get data for highest confirmation count
        for key, value in consensus_data.items():
            num_confirmations = value.get("num_confirmations")
            if num_confirmations >= greatest_num_confirmations:
                greatest_num_confirmations = num_confirmations
                key_for_highest_confirmations = key

        # Check num confirmations reaches min_confirm amount
        total_workers = len(self._get_workers(worker))
        percentage_of_workers = (greatest_num_confirmations / total_workers) * 100
        highest_confirmations = consensus_data.get(key_for_highest_confirmations)
        if percentage_of_workers < min_confirmation:
            raise Exception(
                "Min consensus response did not reach minimum consensus response required"
            )

        return highest_confirmations["data"]

    def _get_workers(self, worker):
        if self.__class__.__name__ == "Network":
            return getattr(self, worker)
        else:
            return getattr(self.network, worker)

    def _get_min_confirmation(self):
        if self.__class__.__name__ == "Network":
            return getattr(self, "min_confirmation")
        else:
            return getattr(self.network, "min_confirmation")
