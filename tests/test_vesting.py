from tests.base_test import BaseTest
from tests.utils import build_client

from zerochain.actions import vesting

ALLOCATION_ID = "296896621095a9d8a51e6e4dba2bdb5661ea94ffd8fdb0a084301bffd81fe7e6"
BLOBBER_ID = "144a94640cb78130434a79a7a12d0b2c85f819e3ea8856db31c7fde30c30a820"


class TestAllocation(BaseTest):
    def setUp(self) -> None:
        self.client = build_client()
        self.mock_dir = "vesting"
        return super().setUp()


# get_vesting_pool_config
# get_vesting_pool_info
# list_vesting_pool_info
# vesting_pool_create
# vesting_pool_delete
# vesting_pool_unlock
# vesting_pool_trigger
# vesting_pool_stop
