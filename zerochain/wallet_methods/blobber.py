from zerochain.const import (
    Endpoints,
)


class BlobberMethods:
    def get_blobber_info(wallet, blobber_id):
        """Get info for given blobber ID"""
        blobbers = wallet.list_blobbers()
        for blobber in blobbers:
            if blobber["id"] == blobber_id:
                found_blobber = blobber
        if not found_blobber:
            return {"error": "Blobber with that ID not found"}
        return found_blobber

    def get_blobber_stats(wallet, blobber_url):
        """Get stats for given blobber url"""
        endpoint = f"{blobber_url}/getstats"
        res = wallet._request(endpoint)
        res = wallet._check_status_code(res)
        return res

    def list_blobbers(wallet):
        """Get stats of each blobber used by the allocation, detailed
        information of allocation size and write markers per blobber"""
        endpoint = Endpoints.SC_BLOBBER_STATS
        res = wallet._consensus_from_workers("sharders", endpoint)
        try:
            nodes = res.get("Nodes")
            return nodes
        except:
            return res

    def list_blobbers_by_allocation_id(wallet, allocation_id):
        """Get stats of each blobber used by the allocation, detailed
        information of allocation size and write markers per blobber"""
        res = wallet.get_allocation_info(allocation_id)
        try:
            return res.get("blobbers")
        except:
            return res
