from datetime import timedelta
import json
from time import time

from zerochain.allocation import Allocation
from zerochain.transaction import Transaction
from zerochain.utils import get_duration_nanoseconds
from zerochain.const import Endpoints, TransactionName, STORAGE_SMART_CONTRACT_ADDRESS


class AllocationConfig:
    DATA_SHARDS = 2
    PARITY_SHARDS = 2
    SIZE = 1628610719
    TOKEN_LOCK = 1
    PREFERRED_BLOBBERS = None
    READ_PRICE = {"min": 0, "max": 9223372036854775807}
    WRITE_PRICE = {"min": 0, "max": 9223372036854775807}
    MAX_CHALLENGE_COMPLETION_TIME = 3600000000000


def get_sc_config(client):
    """Get storage contract config"""
    res = client._consensus_from_workers("sharders", Endpoints.SC_GET_CONFIG)
    return res


def create_read_pool(client):
    input = None
    return client._handle_transaction(
        transaction_name=TransactionName.STORAGESC_CREATE_READ_POOL,
        input=input,
    )


def list_read_pool_info(client, allocation_id=None):
    url = f"{Endpoints.SC_REST_READPOOL_STATS}?client_id={client.id}"
    res = client._consensus_from_workers("sharders", url)

    if allocation_id:
        return filter_by_allocation_id(res, allocation_id)
    else:
        return return_pools(res)


def list_write_pool_info(client, allocation_id=None):
    url = f"{Endpoints.SC_REST_WRITEPOOL_STATS}?client_id={client.id}"
    res = client._consensus_from_workers("sharders", url)
    if allocation_id:
        return filter_by_allocation_id(res, allocation_id)
    else:
        return return_pools(res)


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


def read_pool_unlock(client, pool_id):
    input = {"pool_id": pool_id}
    return client._handle_transaction(
        input=input,
        transaction_name=TransactionName.STORAGESC_READ_POOL_UNLOCK,
    )


def write_pool_lock(
    client, allocation_id, amount, days, hours, minutes, seconds, blobber_id
):
    duration = get_duration_nanoseconds(days, hours, minutes, seconds)
    input = {"duration": duration, "allocation_id": allocation_id}
    if blobber_id:
        input.setdefault("blobber_id", blobber_id)
    return client._handle_transaction(
        input=input,
        value=amount,
        transaction_name=TransactionName.STORAGESC_WRITE_POOL_LOCK,
    )


def write_pool_unlock(client, pool_id):
    input = {"pool_id": pool_id}
    return client._handle_transaction(
        input=input,
        transaction_name=TransactionName.STORAGESC_WRITE_POOL_UNLOCK,
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
    aloc = filter_by_allocation_id(alocs, allocation_id, "list")
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


def update_allocation(
    client,
    allocation_id,
    extend_expiration_hours,
    size,
    set_immutable,
):
    future = int(timedelta(hours=extend_expiration_hours).total_seconds())

    input = {
        "owner_id": client.id,
        "id": allocation_id,
        "size": size,
        "expiration_date": future,
        "set_immutable": set_immutable,
    }

    return client._handle_transaction(
        transaction_name=TransactionName.STORAGESC_UPDATE_ALLOCATION,
        input=input,
        value=1,
    )


# STILL NEED TESTS


def cancel_allocation(client, allocation_id):
    input = {"allocation_id": allocation_id}
    return client._handle_transaction(
        transaction_name=TransactionName.STORAGESC_CANCEL_ALLOCATION,
        input=input,
    )


def finalize_allocation(client, allocation_id):
    input = {"allocation_id": allocation_id}
    return client._handle_transaction(
        transaction_name=TransactionName.STORAGESC_FINALIZE_ALLOCATION,
        input=input,
    )


def add_curator(client, curator_id, allocation_id):
    input = {"curator_id": curator_id, "allocation_id": allocation_id}
    return client._handle_transaction(
        transaction_name=TransactionName.STORAGESC_ADD_CURATOR, input=input
    )


def curator_transafer_allocation(
    client, to_client_id, to_client_public_key, allocation_id
):
    input = {
        "new_owner_id": to_client_id,
        "new_owner_public_key": to_client_public_key,
        "allocation_id": allocation_id,
    }
    return client._handle_transaction(
        transaction_name=TransactionName.STORAGESC_CURATOR_TRANSFER, input=input
    )


# CONFIRM METHODS BELOW


def allocation_min_lock(
    client,
    data_shards=AllocationConfig.DATA_SHARDS,
    parity_shards=AllocationConfig.PARITY_SHARDS,
    size=AllocationConfig.SIZE,
    preferred_blobbers=AllocationConfig.PREFERRED_BLOBBERS,
    write_price=AllocationConfig.WRITE_PRICE,
    read_price=AllocationConfig.READ_PRICE,
    max_challenge_completion_time=AllocationConfig.MAX_CHALLENGE_COMPLETION_TIME,
    expiration_date=time(),
):
    future = int(expiration_date + timedelta(days=30).total_seconds())

    payload = json.dumps(
        {
            "allocation_data": {
                "data_shards": data_shards,
                "parity_shards": parity_shards,
                "owner_id": client.id,
                "owner_public_key": client.public_key,
                "size": size,
                "expiration_date": future,
                "read_price_range": read_price,
                "write_price_range": write_price,
                "max_challenge_completion_time": max_challenge_completion_time,
                "preferred_blobbers": preferred_blobbers,
            },
        }
    )

    res = client._consensus_from_workers(
        "sharders", endpoint=Endpoints.SC_REST_ALLOCATION_MIN_LOCK, data=payload
    )

    return res


# Utility methods


def return_pools(res):
    try:
        return res.get("pools")
    except:
        return res


def filter_by_allocation_id(res, allocation_id, format="dict"):
    pool_info = []
    if format == "list":
        for aloc in res:
            if aloc["id"] == allocation_id:
                return aloc

    elif allocation_id and res["pools"]:
        pools = res["pools"]
        for pool in pools:
            if pool["allocation_id"] == allocation_id:
                pool_info.append(pool)

        if len(pool_info) == 0:
            return []
        else:
            return pool_info
