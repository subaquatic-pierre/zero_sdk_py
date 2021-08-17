from zerochain.const import (
    TransactionName,
    Endpoints,
    INTEREST_POOL_SMART_CONTRACT_ADDRESS,
)


def list_lock_token(client):
    endpoint = f"{Endpoints.GET_LOCKED_TOKENS}?client_id={client.id}"
    empty_return_value = {
        "message": "Failed to get locked tokens.",
        "code": "resource_not_found",
        "error": "resource_not_found: can't find user node",
    }
    res = client._consensus_from_workers(
        "sharders", endpoint, empty_return_value=empty_return_value
    )
    return res


def get_lock_config(client):
    endpoint = Endpoints.GET_LOCK_CONFIG
    res = client._consensus_from_workers("sharders", endpoint)
    return res


def lock_token(client, amount, hours=0, minutes=0):
    if hours < 0 or minutes < 0:
        raise Exception("Invalid time")

    input = {"duration": f"{hours}h{minutes}m"}
    return client._handle_transaction(
        transaction_name=TransactionName.LOCK_TOKEN,
        input=input,
        value=amount,
        sc_address=INTEREST_POOL_SMART_CONTRACT_ADDRESS,
    )


def unlock_token(client, pool_id):
    input = {"pool_id": pool_id}
    return client._handle_transaction(
        transaction_name=TransactionName.UNLOCK_TOKEN,
        input=input,
        sc_address=INTEREST_POOL_SMART_CONTRACT_ADDRESS,
    )
