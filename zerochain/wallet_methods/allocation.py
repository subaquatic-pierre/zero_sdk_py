from datetime import timedelta
from zerochain.allocation import Allocation

from zerochain.utils import get_duration_nanoseconds
from zerochain.const import (
    Endpoints,
    TransactionName,
)


class AllocationMethods:
    def get_sc_config(wallet):
        """Get storage contract config"""
        res = wallet._consensus_from_workers("sharders", Endpoints.SC_GET_CONFIG)
        return res

    def read_pool_lock(
        wallet,
        amount,
        allocation_id,
        days,
        hours,
        minutes,
        seconds,
        blobber_id,
    ):
        duration = get_duration_nanoseconds(days, hours, minutes, seconds=seconds)
        input = {"duration": duration, "allocation_id": allocation_id}
        if blobber_id:
            input["blobber_id"] = blobber_id

        return wallet._handle_transaction(
            input=input,
            transaction_name=TransactionName.STORAGESC_READ_POOL_LOCK,
            value=amount,
        )

    def list_read_pool_by_allocation_id(wallet, allocation_id):
        url = f"{Endpoints.SC_REST_READPOOL_STATS}?client_id={wallet.client_id}"
        res = wallet._consensus_from_workers("sharders", url)

        return wallet._filter_by_allocation_id(res, allocation_id)

    def read_pool_unlock(wallet, pool_id):
        input = {"pool_id": pool_id}
        return wallet._handle_transaction(
            input=input,
            transaction_name=TransactionName.STORAGESC_READ_POOL_UNLOCK,
        )

    def list_allocations(wallet):
        url = f"{Endpoints.SC_REST_ALLOCATIONS}?client={wallet.client_id}"
        res = wallet._consensus_from_workers("sharders", url)
        return res

    def get_allocation_info(wallet, allocation_id):
        url = f"{Endpoints.SC_REST_ALLOCATION}?allocation={allocation_id}"
        res = wallet._consensus_from_workers("sharders", url)
        return res

    def get_allocation(wallet, allocation_id) -> Allocation:
        """Returns an instance of an allocation"""
        alocs = wallet.list_allocations()
        aloc = wallet._filter_by_allocation_id(alocs, allocation_id, "list")
        return Allocation(aloc["id"], wallet)

    def create_allocation(
        wallet,
        data_shards,
        parity_shards,
        size,
        lock_tokens,
        preferred_blobbers,
        write_price,
        read_price,
        max_challenge_completion_time,
        expiration_date,
    ):
        future_date = int(expiration_date + timedelta(days=30).total_seconds())
        input = {
            "data_shards": data_shards,
            "parity_shards": parity_shards,
            "owner_id": wallet.client_id,
            "owner_public_key": wallet.public_key,
            "size": size,
            "expiration_date": future_date,
            "read_price_range": read_price,
            "write_price_range": write_price,
            "max_challenge_completion_time": max_challenge_completion_time,
            "preferred_blobbers": preferred_blobbers,
        }

        data = wallet._handle_transaction(
            transaction_name=TransactionName.NEW_ALLOCATION_REQUEST,
            input=input,
            value=lock_tokens,
        )
        return Allocation(data["hash"], wallet)
