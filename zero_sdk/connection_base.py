from abc import ABC
from zero_sdk.const import Endpoints
from requests import request
import json
from requests.models import Response
from zero_sdk.utils import hash_string
from zero_sdk.exceptions import ConsensusError


class ConnectionBase(ABC):
    def _check_status_code(
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
                    return res.text
        else:
            if raise_exception:
                raise ConnectionError(f"{error_message} - Message: {res.text}")
            else:
                return res.text

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

    def _get_consensus_from_workers(
        self, worker, endpoint, empty_return_value=None
    ) -> dict:
        """Get response from all workers, consolidate responses to get consesus of data,
        return data of highest number of confirmations of a response
        :param worker: String, name of worker to request data,
        :param endpoint: String, endpoint to request from worker
        """
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
            valid_response = self._check_status_code(res)

            # Check if get_balance request and empty wallet, return empty balance value as data
            if type(valid_response) == str:
                valid_response = self._handle_empty_return_value(
                    valid_response, empty_return_value, endpoint
                )

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

        if len(response_hash_map) < 1:
            raise ConsensusError("No consesus reached from workers")

        consensus_data = self._get_consensus_data(response_hash_map, workers)
        return consensus_data

    def _get_consensus_data(self, consensus_data, workers):
        """Take all consensus data, check min required confirmations,
        return highest number of confirmations in data, ensure min confirmation count met
        :param consensus_data: Dict, received from _get_consensus_from_workers
        :param worker: String, string for name of worker
        """
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
        total_workers = len(workers)
        percentage_of_workers = (greatest_num_confirmations / total_workers) * 100
        highest_confirmations = consensus_data.get(key_for_highest_confirmations)
        if percentage_of_workers < min_confirmation:
            raise ConsensusError(
                "Minimum consesus requirement not met, check network config settings or network worker availability"
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

    def _handle_empty_return_value(
        self, valid_response: str, empty_value: dict, endpoint: str
    ):
        try:
            json_res = json.loads(valid_response)
        except Exception:
            json_res = {}

        if Endpoints.GET_BALANCE in endpoint:
            if json_res.get("error") == "value not present":
                valid_response = empty_value

        elif Endpoints.GET_LOCKED_TOKENS in endpoint:
            if json_res.get("code") == "resource_not_found":
                valid_response = empty_value

        return valid_response
