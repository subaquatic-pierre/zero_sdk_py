import json


class MockResponse:
    def __init__(self, status_code, data) -> None:
        self.status_code = status_code
        self.data = data

    def json(self):
        if not self.data:
            raise ConnectionError
        return self.data

    @property
    def text(self):
        if not self.data:
            raise ConnectionError
        return json.dumps(self.data)
