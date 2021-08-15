from zerochain.const import Endpoints, TransactionName, MINER_SMART_CONTRACT_ADDRESS

# Miner settings

miner_pool = {"id": "", "balance": ""}

miner_pool_stats = {
    "delegate_id": "",
    "high": "",
    "low": "",
    "interest_rate": "",
    "total_paid": "",
    "number_rounds": "",
}

miner_delegate_pool = {"stats": miner_pool_stats, "pool": miner_pool}

# ----------


def get_stake_pool_info(client, node_id, pool_id):
    endpoint = f"{Endpoints.GET_MINERSC_POOL_STATS}?id={node_id}&pool_id={pool_id}"
    empty_return_value = {"pools": {}}
    res = client._consensus_from_workers(
        "sharders", endpoint, empty_return_value=empty_return_value
    )
    return res


def list_stake_pool_info(client):
    endpoint = f"{Endpoints.GET_MINERSC_USER_STATS}?client_id={client.id}"
    empty_return_value = {"pools": {}}
    res = client._consensus_from_workers(
        "sharders", endpoint, empty_return_value=empty_return_value
    )
    try:
        return res.get("pools")
    except:
        return res


def miner_lock_token(
    client,
    amount,
    node_id,
):
    """Lock tokens on miner"""
    input = {"id": node_id}
    return client._handle_transaction(
        transaction_name=TransactionName.MINERSC_LOCK,
        input=input,
        value=amount,
        sc_address=MINER_SMART_CONTRACT_ADDRESS,
    )


def miner_unlock_token(client, node_id, pool_id):
    input = {"id": node_id, "pool_id": pool_id}
    return client._handle_transaction(
        transaction_name=TransactionName.MINERSC_UNLOCK,
        input=input,
        sc_address=MINER_SMART_CONTRACT_ADDRESS,
    )


def update_miner_settings(
    self,
    miner_id="",
    miner_url="",
    delegate_client="",
    service_charge=0,
    num_delegates=0,
    min_stake=0,
    max_stake=0,
    block_reward=None,
    service_charge_stat=None,
    users_fee=None,
    block_sharders_fee=None,
    sharder_rewards=None,
    pending_pools=[miner_delegate_pool],
    active_pools=[miner_delegate_pool],
    deleting_pools=[miner_delegate_pool],
):

    miner_stat = {
        "block_reward": block_reward,
        "service_charge": service_charge_stat,
        "users_fee": users_fee,
        "block_sharders_fee": block_sharders_fee,
        "sharder_rewards": sharder_rewards,
    }

    simple_miner_info = {
        "id": miner_id,
        "url": miner_url,
        "delegate_client": delegate_client,
        "service_charge": service_charge,
        "number_of_delegates": num_delegates,
        "min_stake": min_stake,
        "max_stake": max_stake,
        "stat": miner_stat,
    }

    input = {
        "simple_miner": simple_miner_info,
        "pending": pending_pools,
        "active": active_pools,
        "deleting_pools": deleting_pools,
    }

    return self._handle_transaction(
        transaction_name=TransactionName.MINERSC_SETTINGS,
        input=input,
        sc_address=MINER_SMART_CONTRACT_ADDRESS,
    )
