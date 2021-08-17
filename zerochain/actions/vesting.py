from time import time

from zerochain.const import (
    Endpoints,
    TransactionName,
    VESTING_SMART_CONTRACT_ADDRESS,
)


def get_vesting_pool_config(client):
    endpoint = Endpoints.GET_VESTING_CONFIG
    res = client._consensus_from_workers("sharders", endpoint)
    return res


def get_vesting_pool_info(client, pool_id):
    endpoint = f"{Endpoints.GET_VESTING_POOL_INFO}?pool_id={pool_id}"
    res = client._consensus_from_workers("sharders", endpoint)
    return res


def list_vesting_pool_info(client):
    endpoint = f"{Endpoints.GET_VESTING_CLIENT_POOLS}?client_id={client.id}"
    res = client._consensus_from_workers("sharders", endpoint)
    try:
        return res.get("pools")
    except:
        return res


def vesting_pool_create(
    client,
    destinations,
    hours=0,
    minutes=0,
    days=0,
    description="",
    start_time=int(time()),
):
    duration = 140000000000
    # duration = int(
    #     timedelta(days=days, hours=hours, minutes=minutes).total_seconds()
    # )
    input = {
        "description": description,
        "start_time": start_time,
        "duration": duration,
        "destinations": destinations,
    }
    return client._handle_transaction(
        input=input,
        transaction_name=TransactionName.VESTING_ADD,
        sc_address=VESTING_SMART_CONTRACT_ADDRESS,
    )


def vesting_pool_delete(client, pool_id):
    input = {"pool_id": pool_id}
    return client._handle_transaction(
        input=input,
        transaction_name=TransactionName.VESTING_DELETE,
        sc_address=VESTING_SMART_CONTRACT_ADDRESS,
    )


def vesting_pool_unlock(client, pool_id):
    input = {"pool_id": pool_id}
    return client._handle_transaction(
        input=input,
        transaction_name=TransactionName.VESTING_UNLOCK,
        sc_address=VESTING_SMART_CONTRACT_ADDRESS,
    )


def vesting_pool_trigger(client, pool_id):
    input = {"pool_id": pool_id}
    return client._handle_transaction(
        input=input,
        transaction_name=TransactionName.VESTING_TRIGGER,
        sc_address=VESTING_SMART_CONTRACT_ADDRESS,
    )


def vesting_pool_stop(client, miner_id, pool_id):
    input = {"pool_id": pool_id, "destination": miner_id}
    return client._handle_transaction(
        input=input,
        transaction_name=TransactionName.VESTING_STOP,
        sc_address=VESTING_SMART_CONTRACT_ADDRESS,
    )
