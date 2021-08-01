MULTI_SIG_SMART_CONTRACT_ADDRESS = (
    "27b5ef7120252b79f9dd9c05505dd28f328c80f6863ee446daede08a84d651a7"
)
VESTING_SMART_CONTRACT_ADDRESS = (
    "2bba5b05949ea59c80aed3ac3474d7379d3be737e8eb5a968c52295e48333ead"
)
FAUCET_SMART_CONTRACT_ADDRESS = (
    "6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d3"
)
ZRC20_SMART_CONTRACT_ADDRESS = (
    "6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d5"
)
STORAGE_SMART_CONTRACT_ADDRESS = (
    "6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d7"
)
MINER_SMART_CONTRACT_ADDRESS = (
    "6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d9"
)
INTEREST_POOL_SMART_CONTRACT_ADDRESS = (
    "cf8d0df9bd8cc637a4ff4e792ffe3686da6220c45f0e1103baa609f3f1751ef4"
)


class Endpoints:
    REGISTER_CLIENT = "v1/client/put"
    PUT_TRANSACTION = "v1/transaction/put"

    GET_RECENT_FINALIZED = "v1/block/get/recent_finalized"
    GET_LATEST_FINALIZED = "v1/block/get/latest_finalized"
    GET_CHAIN_STATS = "v1/chain/get/stats"
    GET_BLOCK_INFO = "v1/block/get"
    CHECK_TRANSACTION_STATUS = "v1/transaction/get/confirmation"
    GET_BALANCE = "v1/client/get/balance"
    GET_SCSTATE = "v1/scstate/get"

    # SC REST
    SC_REST = "v1/screst/"
    SC_REST_ALLOCATION = "v1/screst/" + STORAGE_SMART_CONTRACT_ADDRESS + "/allocation"
    SC_REST_ALLOCATIONS = "v1/screst/" + STORAGE_SMART_CONTRACT_ADDRESS + "/allocations"
    SC_REST_READPOOL_STATS = (
        "v1/screst/" + STORAGE_SMART_CONTRACT_ADDRESS + "/getReadPoolStat"
    )
    SC_REST_WRITEPOOL_STATS = (
        "v1/screst/" + STORAGE_SMART_CONTRACT_ADDRESS + "/getWritePoolStat"
    )
    SC_BLOBBER_STATS = "v1/screst/" + STORAGE_SMART_CONTRACT_ADDRESS + "/getblobbers"
    SC_SHARDER_LIST = "v1/screst/" + MINER_SMART_CONTRACT_ADDRESS + "/getSharderList"
    SC_MINERS_STATS = "v1/screst/" + MINER_SMART_CONTRACT_ADDRESS + "/getMinerList"
    SC_REST_ALLOCATION_MIN_LOCK = (
        "v1/screst/" + STORAGE_SMART_CONTRACT_ADDRESS + "/allocation_min_lock"
    )

    GET_LOCKED_TOKENS = (
        "v1/screst/" + INTEREST_POOL_SMART_CONTRACT_ADDRESS + "/getPoolsStats"
    )
    GET_USER_POOLS = "v1/screst/" + MINER_SMART_CONTRACT_ADDRESS + "/getUserPools"

    # STAKING
    GET_STORAGESC_POOL_STATS = (
        "v1/screst/" + STORAGE_SMART_CONTRACT_ADDRESS + "/getUserStakePoolStat"
    )
    GET_MINERSC_POOL_STATS = (
        "v1/screst/" + MINER_SMART_CONTRACT_ADDRESS + "/getUserPools"
    )

    # BLOBBER
    ALLOCATION_FILE_LIST = "/v1/file/list/"
    FILE_STATS_ENDPOINT = "/v1/file/stats/"
    OBJECT_TREE_ENDPOINT = "/v1/file/objecttree/"
    FILE_META_ENDPOINT = "/v1/file/meta/"
    RENAME_ENDPOINT = "/v1/file/rename/"
    COPY_ENDPOINT = "/v1/file/copy/"
    UPLOAD_ENDPOINT = "/v1/file/upload/"
    COMMIT_ENDPOINT = "/v1/connection/commit/"
    COPY_ENDPOINT = "/v1/file/copy/"
    OBJECT_TREE_ENDPOINT = "/v1/file/objecttree/"
    COMMIT_META_TXN_ENDPOINT = "/v1/file/commitmetatxn/"

    PROXY_SERVER_UPLOAD_ENDPOINT = "/upload"
    PROXY_SERVER_DOWNLOAD_ENDPOINT = "/download"
    PROXY_SERVER_SHARE_ENDPOINT = "/share"
    PROXY_SERVER_RENAME_ENDPOINT = "/rename"
    PROXY_SERVER_COPY_ENDPOINT = "/copy"
    PROXY_SERVER_DELETE_ENDPOINT = "/delete"
    PROXY_SERVER_MOVE_ENDPOINT = "/move"
    PROXY_SERVER_ENCRYPT_PUBLIC_KEY_ENDPOINT = "/publicEncryptionKey"

    # ZEROBOX URLs
    ZEROBOX_SERVER_GET_MNEMONIC_ENDPOINT = "/getmnemonic"
    ZEROBOX_SERVER_SHARE_INFO_ENDPOINT = "/shareinfo"
    ZEROBOX_SERVER_SAVE_MNEMONIC_ENDPOINT = "/savemnemonic"
    ZEROBOX_SERVER_DELETE_MNEMONIC_ENDPOINT = "/shareinfo"
    ZEROBOX_SERVER_REFERRALS_INFO_ENDPOINT = "/getreferrals"
