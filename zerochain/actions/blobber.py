import json
from zerochain.const import Endpoints, STORAGE_SMART_CONTRACT_ADDRESS
from zerochain.actions import allocation

# def update_blobber_settings(client, blobber_id, )


def get_blobber_info(client, blobber_id):
    """Get info for given blobber ID"""
    blobbers = client.list_blobbers()
    for blobber in blobbers:
        if blobber["id"] == blobber_id:
            found_blobber = blobber
    if not found_blobber:
        return {"error": "Blobber with that ID not found"}
    return found_blobber


def get_blobber_stats(client, blobber_url):
    """Get stats for given blobber url"""
    endpoint = f"{blobber_url}/getstats"
    res = client._request(endpoint)
    res = client._check_status_code(res)
    return res


def list_blobbers(client):
    """Get stats of each blobber used by the allocation, detailed
    information of allocation size and write markers per blobber"""
    endpoint = Endpoints.SC_BLOBBER_STATS
    res = client._consensus_from_workers("sharders", endpoint)
    try:
        nodes = res.get("Nodes")
        return nodes
    except:
        return res


def list_blobbers_by_allocation_id(client, allocation_id):
    """Get stats of each blobber used by the allocation, detailed
    information of allocation size and write markers per blobber"""
    res = allocation.get_allocation_info(client, allocation_id)
    try:
        return res.get("blobbers")
    except:
        return res


def blobber_lock_token(client, transaction_value, blobber_id):
    """Lock tokens on blobber"""
    payload = json.dumps(
        {"name": "stake_pool_lock", "input": {"blobber_id": blobber_id}}
    )
    res = client._execute_smart_contract(
        to_client_id=STORAGE_SMART_CONTRACT_ADDRESS,
        transaction_value=transaction_value,
        payload=payload,
    )
    return res


def blobber_unlock_token(client, pool_id, blobber_id):
    """Unlock tokens from pool id and blobber"""
    payload = json.dumps(
        {
            "name": "stake_pool_unlock",
            "input": {"pool_id": pool_id, "blobber_id": blobber_id},
        }
    )
    res = client._execute_smart_contract(
        to_client_id=STORAGE_SMART_CONTRACT_ADDRESS,
        payload=payload,
    )
    return res
