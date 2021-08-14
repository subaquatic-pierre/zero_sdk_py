class MockWallet:
    def mock_return(return_value):
        def wrapper(self):
            return return_value

        return wrapper
