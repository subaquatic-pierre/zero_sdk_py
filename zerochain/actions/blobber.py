from zerochain.const import (
    Endpoints,
)


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
    res = client.get_allocation_info(allocation_id)
    try:
        return res.get("blobbers")
    except:
        return res
