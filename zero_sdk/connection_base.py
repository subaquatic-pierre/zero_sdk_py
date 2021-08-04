from abc import ABC
from time import sleep
from zero_sdk.const import Endpoints
import requests
from concurrent.futures import ThreadPoolExecutor

import json
from requests.models import Response
from zero_sdk.utils import hash_string, timer
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
                # successful code 200 response
                if return_type == "string":
                    return res.text
                if return_type == "json":
                    return res.json()
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
        try:
            res = requests.request(method, url, headers=headers, data=data, files=files)
            return res
        except requests.exceptions.RequestException as e:
            return e

    def _parallel_requests(
        self,
        workers,
        endpoint,
        method,
        data,
        files,
        headers,
    ):
        future_responses = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            for worker in workers:
                url = f"{worker.url}/{endpoint}"

                future = executor.submit(
                    self._request,
                    method,
                    url,
                    data=data,
                    files=files,
                    headers=headers,
                )
                future_responses.append(future)

        responses = [future.result() for future in future_responses]
        return responses

    def _consensus_from_workers(
        self,
        worker,
        endpoint,
        method="GET",
        data=None,
        files=None,
        headers=None,
        empty_return_value=None,
        min_confirmation=None,
    ) -> dict:
        """Get response from all workers, consolidate responses to get consesus of data,
        return data of highest number of confirmations of a response
        :param worker: String, name of worker to request data,
        :param endpoint: String, endpoint to request from worker
        """
        worker_string = worker
        workers = self._get_workers(worker_string)

        responses = self._parallel_requests(
            workers=workers,
            endpoint=endpoint,
            method=method,
            data=data,
            files=files,
            headers=headers,
        )

        response_hash_map = {}

        # Loop through workers
        for reponse in responses:
            response = self._check_status_code(reponse)

            # Check if get_balance request and empty wallet, return empty balance value as data
            # if type(response) == str:
            response = self._handle_empty_return_value(
                response, empty_return_value, endpoint
            )

            # May be string response if node is down, ensure valid dict object
            # if type(response) == dict:

            # JSON response may contain error, do not add to response map, not valid transaction
            if not type(response) == str:
                if response:
                    err = response.get("error")
                    if err:
                        continue

            # Build response hash string
            response_hash_string = hash_string(json.dumps(response))

            # Check if key exists in response map
            existing_response_key = response_hash_map.get(response_hash_string)

            # Increment consensus count if key exists
            if existing_response_key:
                prev_count = existing_response_key.get("num_confirmations")
                response_hash_map[response_hash_string] = {
                    "data": response,
                    "num_confirmations": prev_count + 1,
                }
            # Add key to response map if does not exists
            else:
                response_hash_map[response_hash_string] = {
                    "data": response,
                    "num_confirmations": 1,
                }

        if len(response_hash_map) < 1:
            raise ConsensusError("No consesus reached from workers")

        consensus_data = self._get_consensus_data(
            response_hash_map, workers, min_confirmation
        )
        return consensus_data

    def _get_consensus_data(self, consensus_data, workers, min_confirmation):
        """Take all consensus data, check min required confirmations,
        return highest number of confirmations in data, ensure min confirmation count met
        :param consensus_data: Dict, received from _consensus_from_workers
        :param worker: String, string for name of worker
        """
        if not min_confirmation:
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

    def _handle_empty_return_value(self, response, empty_value: dict, endpoint: str):
        try:
            json_res = json.loads(response)
        except Exception:
            json_res = {}

        if Endpoints.GET_BALANCE in endpoint:
            if json_res.get("error") == "value not present":
                response = empty_value

        elif Endpoints.GET_LOCKED_TOKENS in endpoint:
            if json_res.get("code") == "resource_not_found":
                response = empty_value

        return response
