from zerochain.const import (
    Endpoints,
    TransactionName,
    TransactionType,
    FAUCET_SMART_CONTRACT_ADDRESS,
)


def get_balance(client, format="default") -> int:
    """Get Client balance
    Return float value of tokens
    """
    endpoint = f"{Endpoints.GET_BALANCE}?client_id={client.id}"
    empty_return_value = {"balance": 0}
    res = client._consensus_from_workers(
        "sharders", endpoint, empty_return_value=empty_return_value
    )
    try:
        bal = res.get("balance")
        if format == "default":
            return bal
        elif format == "human":
            return "%.10f" % (bal / 10000000000)
        else:
            return bal

    except AttributeError:
        return res


def send_token(client, to_client_id, amount, description=""):
    input = description

    return client._handle_transaction(
        transaction_type=TransactionType.SEND,
        input=input,
        value=amount,
        sc_address=to_client_id,
    )


def add_tokens(client):
    input = "give me tokens"
    return client._handle_transaction(
        sc_address=FAUCET_SMART_CONTRACT_ADDRESS,
        transaction_name=TransactionName.ADD_TOKEN,
        input=input,
        value=1,
    )
