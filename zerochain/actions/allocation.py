from datetime import timedelta
from zerochain.allocation import Allocation

from zerochain.utils import get_duration_nanoseconds
from zerochain.const import (
    Endpoints,
    TransactionName,
)


def get_sc_config(client):
    """Get storage contract config"""
    res = client._consensus_from_workers("sharders", Endpoints.SC_GET_CONFIG)
    return res


def read_pool_lock(
    client,
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

    return client._handle_transaction(
        input=input,
        transaction_name=TransactionName.STORAGESC_READ_POOL_LOCK,
        value=amount,
    )


def list_read_pool_by_allocation_id(client, allocation_id):
    url = f"{Endpoints.SC_REST_READPOOL_STATS}?client_id={client.id}"
    res = client._consensus_from_workers("sharders", url)

    return client._filter_by_allocation_id(res, allocation_id)


def read_pool_unlock(client, pool_id):
    input = {"pool_id": pool_id}
    return client._handle_transaction(
        input=input,
        transaction_name=TransactionName.STORAGESC_READ_POOL_UNLOCK,
    )


def list_allocations(client):
    url = f"{Endpoints.SC_REST_ALLOCATIONS}?client={client.id}"
    res = client._consensus_from_workers("sharders", url)
    return res


def get_allocation_info(client, allocation_id):
    url = f"{Endpoints.SC_REST_ALLOCATION}?allocation={allocation_id}"
    res = client._consensus_from_workers("sharders", url)
    return res


def get_allocation(client, allocation_id) -> Allocation:
    """Returns an instance of an allocation"""
    alocs = client.list_allocations()
    aloc = client._filter_by_allocation_id(alocs, allocation_id, "list")
    return Allocation(aloc["id"], client)


def create_allocation(
    client,
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
        "owner_id": client.id,
        "owner_public_key": client.public_key,
        "size": size,
        "expiration_date": future_date,
        "read_price_range": read_price,
        "write_price_range": write_price,
        "max_challenge_completion_time": max_challenge_completion_time,
        "preferred_blobbers": preferred_blobbers,
    }

    data = client._handle_transaction(
        transaction_name=TransactionName.NEW_ALLOCATION_REQUEST,
        input=input,
        value=lock_tokens,
    )
    return Allocation(data["hash"], client)
