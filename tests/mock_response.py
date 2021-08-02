class MockResponse:
    def __init__(self, status_code, data) -> None:
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data
