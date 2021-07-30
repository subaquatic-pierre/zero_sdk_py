from const import MAIN_ALLOCATION_ID
from allocation import Allocation
from wallet import Wallet
from network import Network

wallet = Wallet()
main_alloc = Allocation(MAIN_ALLOCATION_ID, wallet)

assert hasattr(main_alloc, "id"), "Allocation does not have an ID"
assert hasattr(main_alloc, "wallet"), "Wallet was not assigned to allocation"
