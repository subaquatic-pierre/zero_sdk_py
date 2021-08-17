# Python SDK for 0Chain

This is a Python SDK for 0Chain Blockchain network. Below is a mapping from current ZBox and ZClient CLI methods to Python SDK methods

## ZBox CLI method map

| Go SDK             | Python SDK                  | Status           | Description                                               |
| ------------------ | --------------------------- | ---------------- | --------------------------------------------------------- |
| add                |                             | AWAITING NETWORK | Adds free storage assigner                                |
| add-collab         |                             |                  | add collaborator for a file                               |
| addcurator         |                             |                  | Adds a curator to an allocation                           |
| alloc-cancel       | Client.cancel_allocation    | No Tests         | Cancel an allocation                                      |
| alloc-fini         |                             |                  | Finalize an expired allocation                            |
| bl-info            | Client.get_blobber_stats \  | Tested           | Get blobber info                                          |
|                    | Client.get_blobber_info     | Tested           |                                                           |
| bl-update          |                             |                  | Update blobber settings by its delegate_wallet owner      |
| commit             |                             |                  | commit a file changes to chain                            |
| copy               |                             |                  | copy an object(file/folder) to another folder on blobbers |
| cp-info            |                             |                  | Challenge pool information.                               |
| delete             |                             |                  | delete file from blobbers                                 |
| delete-collab      |                             |                  | delete collaborator for a file                            |
| download           |                             |                  | download file from blobbers                               |
| get                | Client.get_allocation_info  | Tested           | Gets the allocation info                                  |
| get-diff           |                             |                  | Get difference of local and allocation root               |
| get-download-cost  |                             |                  | Get downloading cost                                      |
| get-upload-cost    |                             |                  | Get uploading cost                                        |
| getwallet          | Client.get_wallet_info      | No Tests         | Get wallet information                                    |
| list               |                             |                  | list files from blobbers                                  |
| list-all           |                             |                  | list all files from blobbers                              |
| listallocations    | Client.list_allocations     | Tested           | List allocations for the client                           |
| ls-blobbers        | Client.list_blobbers        | Tested           | Show active blobbers in storage SC.                       |
| meta               |                             |                  | get meta data of files from blobbers                      |
| move               |                             |                  | move an object(file/folder) to another folder on blobbers |
| newallocation      | Client.create_allocation    | Tested           | Creates a new allocation                                  |
| register           | Client.create_wallet        | Tested           | Registers the wallet with the blockchain                  |
| rename             |                             |                  | rename an object(file/folder) on blobbers                 |
| rp-create          | Client.create_read_pool     | Unconfirmed      | Create read pool if missing                               |
| rp-info            | Client.list_read_pool_info  | Tested           | Read pool information.                                    |
| rp-lock            | Client.read_pool_lock       | Tested           | Lock some tokens in read pool.                            |
| rp-unlock          | Client.read_pool_unlock     | Tested           | Unlock some expired tokens in a read pool.                |
| sc-config          | Client.get_sc_config        | Tested           | Show storage SC configuration.                            |
| share              |                             |                  | share files from blobbers                                 |
| sign-data          | Client.sign                 | No Tests         | Sign given data                                           |
| sp-info            | NA                          | Awaiting Network | Stake pool information.                                   |
| sp-lock            | NA                          | Awaiting Network | Lock tokens lacking in stake pool.                        |
| sp-pay-interests   | NA                          | Awaiting Network | Pay interests not payed yet.                              |
| sp-unlock          | NA                          | Awaiting Network | Unlock tokens in stake pool.                              |
| sp-user-info       | NA                          | Awaiting Network | Stake pool information for a user.                        |
| start-repair       |                             |                  | start repair file to blobbers                             |
| stats              |                             |                  | stats for file from blobbers                              |
| sync               |                             |                  | Sync files to/from blobbers                               |
| transferallocation |                             |                  | Transfer an allocation between owners                     |
| update             |                             |                  | update file to blobbers                                   |
| update-attributes  |                             |                  | update object attributes on blobbers                      |
| updateallocation   | Client.update_allocation    | Tested           | Updates allocation's expiry and size                      |
| upload             |                             |                  | upload file to blobbers                                   |
| wp-info            | Client.list_write_pool_info | Tested           | Write pool information.                                   |
| wp-lock            | Client.write_pool_lock      | Tested           | Lock some tokens in write pool.                           |
| wp-unlock          | Client.write_pool_unlock    | Tested           | Unlock some expired tokens in a write pool.               |

## ZClient CLI

| Go SDK             | Python SDK                         | Status        | Description                                                       |
| ------------------ | ---------------------------------- | ------------- | ----------------------------------------------------------------- |
| createmswallet     |                                    |               | create multisig wallet                                            |
| faucet             | Client.add_tokens                  | Tested        | Faucet smart contract                                             |
| getbalance         | Client.get_balance                 | Tested        | Get balance from sharders                                         |
| getblobbers        | Client.list_blobbers               | Tested        | Get registered blobbers from sharders                             |
| getid              | Client.get_worker_id               | Tested        | Get Miner or Sharder ID from its URL                              |
| getlockedtokens    | Client.list_lock_token             | Tested        | Get locked tokens                                                 |
| lock               | Client.lock_token                  | Tested        | Lock tokens                                                       |
| lockconfig         | Client.get_lock_config             | Tested        | Get lock configuration                                            |
| ls-miners          | Client.list_miners                 | Tested        | Get list of all active miners fro Miner SC                        |
| ls-sharders        | Client.list_sharders               | Tested        | Get list of all active sharders fro Miner SC                      |
| mn-config          | Client.get_miner_config            | Tested        | Get miner SC global info.                                         |
| mn-info            | Client.get_node_stats              | Tested        | Get miner/sharder info from Miner SC.                             |
| mn-lock            | Client.miner_lock_token            | Unconfirmed   | Add miner/sharder stake.                                          |
| mn-pool-info       | Client.get_stake_pool_info         | Tested        | Get miner/sharder pool info from Miner SC.                        |
| mn-unlock          | Client.miner_unlock_token          | Unconfirmed   | Unlock miner/sharder stake.                                       |
| mn-update-settings | Client.update_miner_settings       | Unconfirmed   | Change miner/sharder settings in Miner SC.                        |
| mn-user-info       | Client.list_stake_pool_info        | Tested        | Get miner/sharder user pools info from Miner SC.                  |
| recoverwallet      | Client.recover_wallet              | Unimplemented | Recover wallet                                                    |
| register           | Client.create_wallet               | Tested        | Registers the wallet with the blockchain                          |
| send               | Client.send_token                  | Tested        | Send ZCN tokens to another wallet                                 |
| unlock             | Client.unlock_token                | Tested        | Unlock tokens                                                     |
| verify             | Client.check_transaction_status    | Tested        | verify transaction                                                |
|                    | Transaction.validate               |               |                                                                   |
|                    |                                    |               |                                                                   |
|                    | ------- AWAITING NETWORK --------- |               |                                                                   |
| vp-add             | Client.create_vesting_pool         | Unconfirmed   | Add a vesting pool                                                |
| vp-config          | Client.get_vesting_pool_config     | Tested        | Check out vesting pool configurations.                            |
| vp-delete          | Client.vesting_pool_delete         | No Tests      | Delete a vesting pool                                             |
| vp-info            | Client.get_vesting_pool_info       | No Tests      | Check out vesting pool information.                               |
| vp-list            | Client.list_vesting_pool_info      | No Tests      | Check out vesting pools list.                                     |
| vp-stop            | Client.vesting_pool_stop           | Unconfirmed   | Stop vesting for one of destinations and unlock tokens not vested |
| vp-trigger         | Client.vesting_pool_trigger        | No Tests      | Trigger a vesting pool work.                                      |
| vp-unlock          | Client.vesting_pool_unlock         | Unconfirmed   | Unlock tokens of a vesting pool                                   |

---

## TODO

- Ensure client is initialized before each method
- Create client init method

---

## Tests Needed

### Classes

#### Client

- all methods

#### Transaction

- test_execute_smart_contract
- test_submit_transaction
- test_process_transaction

#### Allocation

- save_allocation

#### ConnectionBase

- handle_empty_return_value

#### Network

- json
- from_object

### Actions

#### Interest

- all methods

#### Miner

- all methods

#### Allocation

- filter_by_allocation_id

### Utils

- get_duration_nanoseconds

---

#### Hard coded values

- Allocation creation size
- Allocation lock tokens on creation
