from utils import get_home_path
from wallet import Wallet
from allocation import Allocation
from const import MAIN_ALLOCATION_ID, STORAGE_ADDRESS

wallet = Wallet()
main_alloc = Allocation(MAIN_ALLOCATION_ID, wallet, STORAGE_ADDRESS)

path = f"{get_home_path()}/.zcn/uploads/AMAZING.txt"
# main_alloc.upload_file(path)

info = main_alloc.get_allocation_info()
# print(json.dumps(info, indent=4))

results = main_alloc.download_file("/TOPS.txt")
for res in results:
    print(res.text)
