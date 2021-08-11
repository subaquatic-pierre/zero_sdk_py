# Python SDK for 0Chain

## Issue methods

### Class: Wallet

#### Methods

- get_locked_tokens
- create_read_pool
- allocation_min_lock

## Tests to write

#### Network

- get_worker_stats

#### Wallet

- test_execute_smart_contract
- test_submit_transaction

#### Allocation

- get_write_lock_token info
- get_read_lock_token info
- Save allocation

## Hard coded values

- Allocation creation size
- Allocation lock tokens on creation

## ZBox CLI method map

| Go SDK             | Python SDK                     | Status           | Description                                               |
| ------------------ | ------------------------------ | ---------------- | --------------------------------------------------------- |
| add                |                                |                  | Adds free storage assigner                                |
| add-collab         |                                |                  | add collaborator for a file                               |
| addcurator         |                                |                  | Adds a curator to an allocation                           |
| alloc-cancel       |                                |                  | Cancel an allocation                                      |
| alloc-fini         |                                |                  | Finalize an expired allocation                            |
| bl-info            | Allocation.get_blobber_stats   | No Tests         | Get blobber info                                          |
| bl-update          |                                |                  | Update blobber settings by its delegate_wallet owner      |
| commit             |                                |                  | commit a file changes to chain                            |
| copy               |                                |                  | copy an object(file/folder) to another folder on blobbers |
| cp-info            |                                |                  | Challenge pool information.                               |
| delete             |                                |                  | delete file from blobbers                                 |
| delete-collab      |                                |                  | delete collaborator for a file                            |
| download           |                                |                  | download file from blobbers                               |
| get                | Allocation.get_allocation_info | Tested           | Gets the allocation info                                  |
| get-diff           |                                |                  | Get difference of local and allocation root               |
| get-download-cost  |                                |                  | Get downloading cost                                      |
| get-upload-cost    |                                |                  | Get uploading cost                                        |
| getwallet          |                                |                  | Get wallet information                                    |
| list               |                                |                  | list files from blobbers                                  |
| list-all           |                                |                  | list all files from blobbers                              |
| listallocations    | Wallet.list_allocations        | Tested           | List allocations for the client                           |
| ls-blobbers        |                                |                  | Show active blobbers in storage SC.                       |
| meta               |                                |                  | get meta data of files from blobbers                      |
| move               |                                |                  | move an object(file/folder) to another folder on blobbers |
| newallocation      | Wallet.create_allocation       | Tested           | Creates a new allocation                                  |
| register           | Network.create_wallet          | Tested           | Registers the wallet with the blockchain                  |
| rename             |                                |                  | rename an object(file/folder) on blobbers                 |
| rp-create          | Wallet.create_read_pool        |                  | Create read pool if missing                               |
| rp-info            | Wallet.read_pool_info          |                  | Read pool information.                                    |
| rp-lock            |                                |                  | Lock some tokens in read pool.                            |
| rp-unlock          |                                |                  | Unlock some expired tokens in a read pool.                |
| sc-config          |                                |                  | Show storage SC configuration.                            |
| share              |                                |                  | share files from blobbers                                 |
| sign-data          |                                |                  | Sign given data                                           |
| sp-info            | NA                             | Awaiting Network | Stake pool information.                                   |
| sp-lock            | NA                             | Awaiting Network | Lock tokens lacking in stake pool.                        |
| sp-pay-interests   | NA                             | Awaiting Network | Pay interests not payed yet.                              |
| sp-unlock          | NA                             | Awaiting Network | Unlock tokens in stake pool.                              |
| sp-user-info       | NA                             | Awaiting Network | Stake pool information for a user.                        |
| start-repair       |                                |                  | start repair file to blobbers                             |
| stats              |                                |                  | stats for file from blobbers                              |
| sync               |                                |                  | Sync files to/from blobbers                               |
| transferallocation |                                |                  | Transfer an allocation between owners                     |
| update             |                                |                  | update file to blobbers                                   |
| update-attributes  |                                |                  | update object attributes on blobbers                      |
| updateallocation   | Wallet.update_allocation       | Unconfirmed      | Updates allocation's expiry and size                      |
| upload             |                                |                  | upload file to blobbers                                   |
| version            |                                |                  | Prints version information                                |
| wp-info            | Allocation.get_write_pool_info | Tested           | Write pool information.                                   |
| wp-lock            | Allocation.lock_write_tokens   | Unimplemented    | Lock some tokens in write pool.                           |
| wp-unlock          |                                |                  | Unlock some expired tokens in a write pool.               |

## ZWallet CLI

| Go SDK             | Python SDK               | Status   | Description                                                       |
| ------------------ | ------------------------ | -------- | ----------------------------------------------------------------- |
| createmswallet     | Network.create_wallet    | Tested   | create multisig wallet                                            |
| faucet             | Wallet.add_tokens        | Tested   | Faucet smart contract                                             |
| getbalance         | Wallet.get_balance       | Tested   | Get balance from sharders                                         |
| getblobbers        |                          |          | Get registered blobbers from sharders                             |
| getid              |                          |          | Get Miner or Sharder ID from its URL                              |
| getlockedtokens    |                          |          | Get locked tokens                                                 |
| help               |                          |          | Help about any command                                            |
| lock               |                          |          | Lock tokens                                                       |
| lockconfig         |                          |          | Get lock configuration                                            |
| ls-miners          | Network.get_miner_list   | No Tests | Get list of all active miners fro Miner SC                        |
| ls-sharders        | Network.get_sharder_list | No Tests | Get list of all active sharders fro Miner SC                      |
| mn-config          | Network.get_miner_config | No Tests | Get miner SC global info.                                         |
| mn-info            | Network.get_node_stats   | No Tests | Get miner/sharder info from Miner SC.                             |
| mn-lock            |                          |          | Add miner/sharder stake.                                          |
| mn-pool-info       |                          |          | Get miner/sharder pool info from Miner SC.                        |
| mn-unlock          |                          |          | Unlock miner/sharder stake.                                       |
| mn-update-settings |                          |          | Change miner/sharder settings in Miner SC.                        |
| mn-user-info       |                          |          | Get miner/sharder user pools info from Miner SC.                  |
| recoverwallet      | Network.recover_wallet   | Tested   | Recover wallet                                                    |
| register           | Network.register         | No Tests | Registers the wallet with the blockchain                          |
| send               |                          |          | Send ZCN tokens to another wallet                                 |
| unlock             |                          |          | Unlock tokens                                                     |
| verify             |                          |          | verify transaction                                                |
| version            |                          |          | Prints version information                                        |
| vp-add             |                          |          | Add a vesting pool                                                |
| vp-config          |                          |          | Check out vesting pool configurations.                            |
| vp-delete          |                          |          | Delete a vesting pool                                             |
| vp-info            |                          |          | Check out vesting pool information.                               |
| vp-list            |                          |          | Check out vesting pools list.                                     |
| vp-stop            |                          |          | Stop vesting for one of destinations and unlock tokens not vested |
| vp-trigger         |                          |          | Trigger a vesting pool work.                                      |
| vp-unlock          |                          |          | Unlock tokens of a vesting pool                                   |
