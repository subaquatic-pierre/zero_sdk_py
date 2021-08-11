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


class TransactionName:
    NEW_ALLOCATION_REQUEST = "new_allocation_request"
    NEW_FREE_ALLOCATION = "free_allocation_request"
    UPDATE_ALLOCATION_REQUEST = "update_allocation_request"
    FREE_UPDATE_ALLOCATION = "free_update_allocation"
    LOCK_TOKEN = "lock"
    UNLOCK_TOKEN = "unlock"

    ADD_FREE_ALLOCATION_ASSIGNER = "add_free_storage_assigner"

    #  Vesting SC
    VESTING_TRIGGER = "trigger"
    VESTING_STOP = "stop"
    VESTING_UNLOCK = "unlock"
    VESTING_ADD = "add"
    VESTING_DELETE = "delete"
    VESTING_UPDATE_CONFIG = "update_config"

    #  Storage SC
    STORAGESC_FINALIZE_ALLOCATION = "finalize_allocation"
    STORAGESC_CANCEL_ALLOCATION = "cancel_allocation"
    STORAGESC_CREATE_ALLOCATION = "new_allocation_request"
    STORAGESC_CREATE_READ_POOL = "new_read_pool"
    STORAGESC_READ_POOL_LOCK = "read_pool_lock"
    STORAGESC_READ_POOL_UNLOCK = "read_pool_unlock"
    STORAGESC_STAKE_POOL_LOCK = "stake_pool_lock"
    STORAGESC_STAKE_POOL_UNLOCK = "stake_pool_unlock"
    STORAGESC_STAKE_POOL_PAY_INTERESTS = "stake_pool_pay_interests"
    STORAGESC_UPDATE_BLOBBER_SETTINGS = "update_blobber_settings"
    STORAGESC_UPDATE_ALLOCATION = "update_allocation_request"
    STORAGESC_WRITE_POOL_LOCK = "write_pool_lock"
    STORAGESC_WRITE_POOL_UNLOCK = "write_pool_unlock"
    STORAGESC_ADD_CURATOR = "add_curator"
    STORAGESC_CURATOR_TRANSFER = "curator_transfer_allocation"

    ADD_TOKEN = "pour"

    #  Miner SC
    MINERSC_LOCK = "addToDelegatePool"
    MINERSC_UNLOCK = "deleteFromDelegatePool"
    MINERSC_SETTINGS = "update_settings"


class TransactionType:
    SEND = 0
    DATA = 10
    # STORAGE_WRITE = 101,
    # STORAGE_READ  = 103,
    SMART_CONTRACT = 1000


class Endpoints:
    NETWORK_DNS = "dns/network"
    REGISTER_CLIENT = "v1/client/put"
    PUT_TRANSACTION = "v1/transaction/put"

    GET_RECENT_FINALIZED = "v1/block/get/recent_finalized"
    GET_LATEST_FINALIZED_BLOCK = "v1/block/get/latest_finalized"
    GET_LATEST_FINALIZED_MAGIC_BLOCK = "v1/block/get/latest_finalized_magic_block"
    GET_LATEST_FINALIZED_MAGIC_BLOCK_SUMMARY = (
        "v1/block/get/latest_finalized_magic_block_summary"
    )
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
    SC_CONFIGS = "v1/screst/" + MINER_SMART_CONTRACT_ADDRESS + "/configs"
    SC_NODE_STAT = "v1/screst/" + MINER_SMART_CONTRACT_ADDRESS + "/nodeStat"
    SC_REST_ALLOCATION_MIN_LOCK = (
        "v1/screst/" + STORAGE_SMART_CONTRACT_ADDRESS + "/allocation_min_lock"
    )

    # INTEREST POOL
    GET_LOCKED_TOKENS = (
        "v1/screst/" + INTEREST_POOL_SMART_CONTRACT_ADDRESS + "/getPoolsStats"
    )
    GET_LOCK_CONFIG = (
        "v1/screst/" + INTEREST_POOL_SMART_CONTRACT_ADDRESS + "/getLockConfig"
    )

    # STAKING
    GET_STORAGESC_POOL_STATS = (
        "v1/screst/" + STORAGE_SMART_CONTRACT_ADDRESS + "/getUserStakePoolStat"
    )
    GET_MINERSC_USER_STATS = (
        "v1/screst/" + MINER_SMART_CONTRACT_ADDRESS + "/getUserPools"
    )
    GET_MINERSC_POOL_STATS = (
        "v1/screst/" + MINER_SMART_CONTRACT_ADDRESS + "/nodePoolStat"
    )

    # VESTING
    VP_GET_CONFIG = "v1/screst/" + VESTING_SMART_CONTRACT_ADDRESS + "/getConfig"

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


class AllocationConfig:
    DATA_SHARDS = 2
    PARITY_SHARDS = 2
    SIZE = 1628610719
    TOKEN_LOCK = 20000000000
    PREFERRED_BLOBBERS = None
    READ_PRICE = {"min": 0, "max": 9223372036854775807}
    WRITE_PRICE = {"min": 0, "max": 9223372036854775807}
    MAX_CHALLENGE_COMPLETION_TIME = 3600000000000


#   "dataShards" : 4,
#   "parityShards" : 2,
#   "allocationSize" : 2,
#   "tokenLock": 5000000000,
#   "tokenLockDuration": "720h",
#   "maxChallengeCompletionTime":3600,
#   "chain_id" :   "0afc093ffb509f059c55478bc1a60351cef7b4e9c008a53a6cc8241ca8617dfe",
#   "clusterName" : "0chain-local-cluster",
#   "proxyServerUrl" : "https://beta.0chain.net/proxy",
#   "recorderUrl": "https://beta.0chain.net/recorder",
#   "zeroBoxUrl": "https://0box.beta.0chain.net",
#   "backend": "https://backend.0chain.net",
#   "dataSource": "database",
#   "explorerType": "public",
#   "transaction_timeout" : 20,
#   "state " : true,
#   "minLockDemand": 0.1
