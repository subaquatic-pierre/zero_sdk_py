import json

from zerochain.const import Endpoints, STORAGE_SMART_CONTRACT_ADDRESS
from zerochain.utils import generate_mnemonic, create_wallet_util, request_dns_workers
from zerochain.bls import generate_keys


def list_miners(client):
    endpoint = Endpoints.SC_MINERS_STATS
    res = client._consensus_from_workers("miners", endpoint)
    try:
        miners = res.get("Nodes")
        return miners
    except:
        return res


def get_miner_config(client):
    endpoint = Endpoints.SC_CONFIGS
    res = client._consensus_from_workers("sharders", endpoint)
    return res


def get_node_stats(client, node_id=None):
    if not node_id:
        raise Exception("Please provide node ID")
    endpoint = f"{Endpoints.SC_NODE_STAT}?id={node_id}"
    res = client._consensus_from_workers("sharders", endpoint)
    return res


def list_sharders(client):
    res = client.get_latest_finalized_magic_block()
    try:
        sharders = res.get("magic_block").get("sharders").get("nodes")
        return sharders
    except:
        return {"error": "not found"}


def get_chain_stats(client):
    endpoint = Endpoints.GET_CHAIN_STATS
    res = client._consensus_from_workers("sharders", endpoint)
    return res


def get_block_by_hash(client, block_id):
    endpoint = f"{Endpoints.GET_BLOCK_INFO}?block={block_id}"
    res = client._consensus_from_workers("sharders", endpoint)
    return res


def get_block_by_round(client, round_num):
    endpoint = f"{Endpoints.GET_BLOCK_INFO}?round={round_num}"
    res = client._consensus_from_workers("sharders", endpoint)
    return res


def get_latest_finalized_block(client):
    endpoint = Endpoints.GET_LATEST_FINALIZED_BLOCK
    res = client._consensus_from_workers("sharders", endpoint)
    return res


def get_latest_finalized_magic_block(client):
    endpoint = Endpoints.GET_LATEST_FINALIZED_MAGIC_BLOCK
    res = client._consensus_from_workers("sharders", endpoint)
    return res


def get_latest_finalized_magic_block_summary(client):
    endpoint = Endpoints.GET_LATEST_FINALIZED_MAGIC_BLOCK_SUMMARY
    res = client._consensus_from_workers("miners", endpoint)
    return res


def check_transaction_status(client, hash):
    endpoint = f"{Endpoints.CHECK_TRANSACTION_STATUS}?hash={hash}"
    res = client._consensus_from_workers("sharders", endpoint)
    return res


def get_worker_stats(client, worker):
    details = {}
    workers = client._get_workers(worker)
    for worker in workers:
        url = f"{worker.url}/_nh/whoami"
        res = client._request(url)
        valid_data = client._check_status_code(res)
        details.setdefault(worker.url, valid_data)

    return details


def get_worker_id(client, worker_url):
    details = {}
    url = f"{worker_url}/_nh/whoami"
    res = client._request(url)
    valid_data = client._check_status_code(res)
    details.setdefault(worker_url, valid_data)

    return details


def create_wallet(network, return_instance=True):
    mnemonic = generate_mnemonic()
    keys = generate_keys(mnemonic)
    res = register_wallet(keys, network)
    data = {
        "client_id": res["id"],
        "client_key": keys["public_key"],
        "keys": [
            {
                "public_key": keys["public_key"],
                "private_key": keys["private_key"],
            }
        ],
        "mnemonic": mnemonic,
        "version": res["version"],
        "date_created": res["creation_date"],
    }
    if return_instance:
        return create_wallet_util(data, network)
    else:
        return res


# def restore_wallet(mnemonic, network, return_instance=True):
#     keys = generate_keys(mnemonic)
#     res = register_wallet(keys, network)
#     data = {
#         "client_id": res["id"],
#         "client_key": keys["public_key"],
#         "keys": [
#             {
#                 "public_key": keys["public_key"],
#                 "private_key": keys["private_key"],
#             }
#         ],
#         "mnemonic": mnemonic,
#         "version": res["version"],
#         "date_created": res["creation_date"],
#     }
#     if return_instance:
#         return create_wallet_util(data, network)
#     else:
#         return res


def register_wallet(keys, network):
    payload = json.dumps(
        {
            "id": keys["client_id"],
            "version": None,
            "creation_date": None,
            "public_key": keys["public_key"],
        }
    )
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    res = network._consensus_from_workers(
        "miners",
        endpoint=Endpoints.register_wallet,
        method="PUT",
        data=payload,
        headers=headers,
        min_confirmation=10,
    )
    return res


def get_storage_smartcontract_for_key(client, key_name, key_value):
    pass


def list_network_dns(client):
    return request_dns_workers(url=client.hostname)
