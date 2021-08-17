import json
from abc import ABC
from time import sleep
from requests.models import Response
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from zerochain.const import Endpoints
from zerochain.utils import hash_string
from zerochain.exceptions import ConsensusError


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

    def _request(
        self, url, method="GET", headers=None, data=None, files=None
    ) -> Response:
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

    def _append_response_to_consensus_data(self, response_data, consensus_data):
        """Build consensus data as each response comes in"""
        confirmation_weight = self._calculate_confirmation_weighting(response_data)

        # Build response hash string
        response_hash_string = hash_string(json.dumps(response_data))

        # Check if key exists in response map
        existing_response_key = consensus_data.get(response_hash_string)

        # Increment consensus count if key exists
        if existing_response_key:
            prev_count = existing_response_key.get("num_confirmations")
            consensus_data[response_hash_string] = {
                "data": response_data,
                "num_confirmations": prev_count + confirmation_weight,
            }
        # Add key to response map if does not exists
        else:
            consensus_data[response_hash_string] = {
                "data": response_data,
                "num_confirmations": confirmation_weight,
            }

    def _check_highest_consensus(self, consensus_data, num_total_workers=0):
        """Check consensus data for highest confirmation count,
        return object and percentage of confirmations"""
        greatest_num_confirmations = 0
        key_for_highest_confirmations = ""

        # Get data for highest confirmation count
        for key, value in consensus_data.items():
            num_confirmations = value.get("num_confirmations")
            if num_confirmations >= greatest_num_confirmations:
                greatest_num_confirmations = num_confirmations
                key_for_highest_confirmations = key

        # Check num confirmations reaches min_confirm amount
        percentage_confirmations = (
            greatest_num_confirmations / num_total_workers
        ) * 100
        highest_confirmations = consensus_data.get(key_for_highest_confirmations)

        return (percentage_confirmations, highest_confirmations.get("data"))

    # -----------------------------------------------------

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
        if not min_confirmation:
            min_confirmation = self._get_min_confirmation()
        worker_string = worker
        workers = self._get_workers(worker_string)
        num_requests = 0

        future_responses = []
        consensus_data = {}

        with ThreadPoolExecutor(max_workers=10) as executor:
            for worker in workers:
                url = f"{worker.url}/{endpoint}"
                future = executor.submit(
                    self._request,
                    method=method,
                    url=url,
                    data=data,
                    files=files,
                    headers=headers,
                )

                future_responses.append(future)

            for future in as_completed(future_responses):
                response = future.result()

                # Error checking and parsing
                response_data = self._check_status_code(response)
                response_data = self._handle_empty_return_value(
                    response_data, empty_return_value, endpoint
                )

                # Build consesus data object
                num_requests += 1
                self._append_response_to_consensus_data(response_data, consensus_data)

                # Check highest percentage of consensus as each future is completed
                percentage_consensus, highest_consensus = self._check_highest_consensus(
                    consensus_data, len(workers)
                )

                # Raise exception if minimum consensus not acheived
                is_min_consensus_reached = self._check_min_consensus_achieved(
                    percentage_consensus, min_confirmation, num_requests, len(workers)
                )

                if is_min_consensus_reached:
                    executor.shutdown(wait=False)
                    return highest_consensus

    def _calculate_confirmation_weighting(
        self, response_data, endpoint="", current_weighting=1
    ):
        if (
            type(response_data) == str
            and "entity_not_found" not in response_data
            and "whoami" not in endpoint
        ):
            weight = current_weighting / 2
            return weight
        return current_weighting

    def _check_min_consensus_achieved(
        self, percentage_consensus, min_confirmation, num_requests, num_workers
    ):
        if num_requests >= num_workers:
            if int(percentage_consensus) < min_confirmation:
                raise ConsensusError(
                    "Minimum consesus requirement not met, check network config settings or network worker availability"
                )
        else:
            if int(percentage_consensus) > min_confirmation:
                return True

        return False

    def _get_workers(self, worker):
        if self.__class__.__name__ == "Network":
            return getattr(self, worker)
        elif self.__class__.__name__ == "Allocation":
            return getattr(self.client.network, worker)
        else:
            return getattr(self.network, worker)

    def _get_min_confirmation(self):
        if self.__class__.__name__ == "Network":
            return getattr(self, "min_confirmation")
        elif self.__class__.__name__ == "Allocation":
            return getattr(self.client.network, "min_confirmation")
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
