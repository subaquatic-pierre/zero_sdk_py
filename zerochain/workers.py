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
