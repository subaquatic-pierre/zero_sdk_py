class MockClient:
    def mock_return(return_value):
        def wrapper(self, *args, **kwargs):
            return return_value

        return wrapper
