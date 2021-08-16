class Sharder:
    def __init__(self, sharder_url) -> None:
        self.url = sharder_url


class Miner:
    def __init__(self, miner_url) -> None:
        self.url = miner_url


class Blobber:
    def __init__(self, blobber_url, blobber_id=None) -> None:
        self.url = blobber_url
        self.id = blobber_id

    @staticmethod
    def get_struct(self):
        blobber = {
            "id": "",
            "url": "",
            "public_key": "-",
            "terms": {
                "read_price": 175350921,
                "write_price": 175350921,
                "min_lock_demand": 0.1,
                "max_offer_duration": 2678400000000000,
                "challenge_completion_time": 120000000000,
            },
            "capacity": 1073741824000,
            "used": 155906743618,
            "last_health_check": 1629102674,
            "stake_pool_settings": {
                "delegate_wallet": "",
                "min_stake": 10000000000,
                "max_stake": 1000000000000,
                "num_delegates": 50,
                "service_charge": 0.3,
            },
        }

        return blobber
