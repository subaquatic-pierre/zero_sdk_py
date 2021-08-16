import os
from pathlib import Path
from time import time
import json

from zerochain.connection import ConnectionBase
from zerochain.allocation import Allocation
from zerochain.transaction import Transaction
from zerochain.network import Network
from zerochain.actions import (
    miner,
    vesting,
    allocation,
    blobber,
    interest,
    wallet,
    network,
)
from zerochain.actions.allocation import AllocationConfig
from zerochain.actions.miner import miner_delegate_pool

from zerochain.utils import generate_random_letters
from zerochain.bls import sign_payload
from zerochain.const import (
    STORAGE_SMART_CONTRACT_ADDRESS,
    TransactionType,
)


class Client(ConnectionBase):
    def __init__(
        self,
        client_id,
        client_key,
        public_key,
        private_key,
        mnemonic,
        date_created,
        network,
        version="1.0",
    ):
        self.id = client_id
        self.client_key = client_key
        self.public_key = public_key
        self.private_key = private_key
        self.mnemonic = mnemonic
        self.version = version
        self.date_created = date_created
        self.network = network

    # --------------
    # Wallet Methods
    # --------------

    def get_balance(self, format="default") -> int:
        return wallet.get_balance(self, format)

    def send_token(self, to_client_id, amount, description=""):
        return wallet.send_token(self, to_client_id, amount, description)

    def add_tokens(self):
        return wallet.add_tokens(self)

    # --------------
    # Interest Methods
    # --------------

    def list_lock_token(self):
        return interest.list_lock_token(self)

    def get_lock_config(self):
        return interest.get_lock_config(self)

    def lock_token(self, amount, hours=0, minutes=0):
        return interest.lock_token(self, amount, hours, minutes)

    def unlock_token(self, pool_id):
        return interest.unlock_token(self, pool_id)

    # --------------------
    # Miner methods
    # --------------------

    def list_miners(self):
        return self.network.list_miners()

    def list_sharders(self):
        return self.network.list_sharders()

    def get_stake_pool_info(self, node_id, pool_id):
        return miner.get_stake_pool_info(self, node_id, pool_id)

    def list_stake_pool_info(self):
        return miner.list_stake_pool_info(self)

    def miner_lock_token(
        self,
        amount,
        node_id,
    ):
        return miner.miner_lock_token(self, amount, node_id)

    def miner_unlock_token(self, node_id, pool_id):
        return miner.miner_unlock_token(
            self,
        )

    # --------------------
    # Vesting Pool methods
    # --------------------

    def get_vesting_pool_config(self):
        return vesting.get_vesting_pool_config(self)

    def get_vesting_pool_info(self, pool_id):
        return vesting.get_vesting_pool_config(self, pool_id)

    def list_vesting_pool_info(self):
        return vesting.list_vesting_pool_info(self)

    def vesting_pool_create(
        self,
        destinations,
        hours=0,
        minutes=0,
        days=0,
        description="",
        start_time=int(time()),
    ):
        return vesting.vesting_pool_create(
            self, destinations, hours, minutes, days, description, start_time
        )

    def vesting_pool_delete(self, pool_id):
        return vesting.vesting_pool_delete(self, pool_id)

    def vesting_pool_unlock(self, pool_id):
        return vesting.vesting_pool_unlock(self, pool_id)

    def vesting_pool_trigger(self, pool_id):
        return vesting.vesting_pool_trigger(self, pool_id)

    def vesting_pool_stop(self, miner_id, pool_id):
        return vesting.vesting_pool_stop(self, miner_id, pool_id)

    # --------------------
    # Allocation methods
    # --------------------

    def get_sc_config(self):
        return allocation.get_sc_config(self)

    def list_read_pool_info(self):
        return allocation.list_read_pool_info(self)

    def list_write_pool_info(self):
        return allocation.list_write_pool_info(self)

    def write_pool_lock(self):
        pass
        # return allocation.write_pool_lock(self)

    def write_pool_unlock(self):
        pass
        # return allocation.write_pool_unlock(self)

    def create_read_pool(self):
        return allocation.create_read_pool(self)

    def read_pool_lock(
        self,
        amount,
        allocation_id,
        days=0,
        hours=0,
        minutes=0,
        seconds=0,
        blobber_id=None,
    ):
        return allocation.read_pool_lock(
            self, amount, allocation_id, days, hours, minutes, seconds, blobber_id
        )

    def list_read_pool_by_allocation_id(self, allocation_id):
        return allocation.list_read_pool_by_allocation_id(self, allocation_id)

    def read_pool_unlock(self, pool_id):
        return allocation.read_pool_unlock(self, pool_id)

    def list_allocations(self):
        return allocation.list_allocations(self)

    def get_allocation_info(self, allocation_id):
        return allocation.get_allocation_info(self, allocation_id)

    def get_allocation(self, allocation_id) -> Allocation:
        """Returns an instance of an allocation"""
        return allocation.get_allocation(self, allocation_id)

    def create_allocation(
        self,
        data_shards=AllocationConfig.DATA_SHARDS,
        parity_shards=AllocationConfig.PARITY_SHARDS,
        size=AllocationConfig.SIZE,
        lock_tokens=AllocationConfig.TOKEN_LOCK,
        preferred_blobbers=AllocationConfig.PREFERRED_BLOBBERS,
        write_price=AllocationConfig.WRITE_PRICE,
        read_price=AllocationConfig.READ_PRICE,
        max_challenge_completion_time=AllocationConfig.MAX_CHALLENGE_COMPLETION_TIME,
        expiration_date=time(),
    ):
        return allocation.create_allocation(
            self,
            data_shards,
            parity_shards,
            size,
            lock_tokens,
            preferred_blobbers,
            write_price,
            read_price,
            max_challenge_completion_time,
            expiration_date,
        )

    # --------------------
    # Blobber methods
    # --------------------

    def get_blobber_info(self, blobber_id):
        return blobber.get_blobber_info(self, blobber_id)

    def get_blobber_stats(self, blobber_url):
        return blobber.get_blobber_info(self, blobber_url)

    def list_blobbers(self):
        return blobber.list_blobbers(self)

    def list_blobbers_by_allocation_id(self, allocation_id):
        return blobber.list_blobbers_by_allocation_id(self, allocation_id)

    def blobber_lock_token(self, transaction_value, blobber_id):
        return blobber.blobber_lock_token(self, transaction_value, blobber_id)

    def blobber_unlock_token(self, pool_id, blobber_id):
        return blobber.blobber_unlock_token(self, pool_id, blobber_id)

    def update_blobber_settings(self, blobber_id, settings={}):
        return blobber.update_blobber_settings(self, blobber_id, settings)

    # --------------------
    # Network methods
    # --------------------

    def list_network_dns(self):
        return network.request_dns_workers(url=self.hostname)

    def list_miners(self):
        return network.list_miners(self)

    def get_miner_config(self):
        return network.get_miner_config(self)

    def get_node_stats(self, node_id=None):
        return network.get_node_stats(self, node_id)

    def list_sharders(self):
        return network.list_sharders(self)

    def get_miner_list(self):
        return network.get_miner_list(self)

    def get_chain_stats(self):
        return network.get_chain_stats(self)

    def get_block_by_hash(self, block_id):
        return network.get_block_by_hash(self, block_id)

    def get_block_by_round(self, round_num):
        return network.get_block_by_round(self, round_num)

    def get_latest_finalized_block(self):
        return network.get_latest_finalized_block(self)

    def get_latest_finalized_magic_block(self):
        return network.get_latest_finalized_magic_block(self)

    def get_latest_finalized_magic_block_summary(self):
        return network.get_latest_finalized_magic_block_summary(self)

    def check_transaction_status(self, hash):
        return network.check_transaction_status(self, hash)

    def get_worker_stats(self, worker):
        return network.get_worker_stats(self, worker)

    def get_worker_id(self, worker_url):
        return network.get_worker_id(self, worker_url)

    def get_storage_smartcontract_for_key(self, key_name, key_value):
        return network.get_storage_smartcontract_for_key(self, key_name, key_value)

    @staticmethod
    def create_client(network_param):
        return network.create_client(network_param)

    @staticmethod
    def restore_client(mnemonic):
        return network.restore_client(mnemonic)

    @staticmethod
    def register_client(keys, network_param):
        return network.register_client(keys, network_param)

    # --------------------
    # Utility methods
    # --------------------

    def sign(self, payload):
        return sign_payload(self.private_key, payload)

    def save(self, client_name=None):
        if not client_name:
            client_name = generate_random_letters()

        data = {
            "client_id": self.id,
            "client_key": self.public_key,
            "keys": [{"public_key": self.public_key, "private_key": self.private_key}],
            "mnemonic": self.mnemonic,
            "version": self.version,
            "date_created": self.date_created,
        }

        with open(
            os.path.join(Path.home(), f".zcn/test_clients/client_{client_name}.json"),
            "w",
        ) as f:
            f.write(json.dumps(data, indent=4))

    def get_client_info(self):
        return {
            "client_id": self.id,
            "public_key": self.public_key,
        }

    # --------------
    # Private Methods
    # --------------

    def _handle_transaction(
        self,
        input,
        transaction_name=None,
        transaction_type=TransactionType.SMART_CONTRACT,
        value=0,
        sc_address=STORAGE_SMART_CONTRACT_ADDRESS,
        raise_exception=False,
    ):
        return Transaction.process_transaction(
            transaction_name=transaction_name,
            transaction_type=transaction_type,
            input=input,
            client=self,
            value=value,
            sc_address=sc_address,
            raise_exception=raise_exception,
        )

    @staticmethod
    def from_object(config: dict, network: Network):
        """Returns fully configured instance of client
        :param config: Client config object from json.loads function
        :param network: Instance of configured network
        """
        return Client(
            config.get("client_id"),
            config.get("client_key"),
            config.get("keys")[0]["public_key"],
            config.get("keys")[0]["private_key"],
            config.get("mnemonics"),
            config.get("date_created"),
            network,
            config.get("version"),
        )

    def __repr__(self):
        return f"Client(config, network)"

    def __str__(self):
        return f"client_id: {self.id} \nnetwork_url: {self.network.hostname}"

    # -----------------
    # TODO: Fix methods
    # All below methods need confirmation
    # -----------------

    def update_miner_settings(
        self,
        miner_id="",
        miner_url="",
        delegate_client="",
        service_charge=0,
        num_delegates=0,
        min_stake=0,
        max_stake=0,
        block_reward=None,
        service_charge_stat=None,
        users_fee=None,
        block_sharders_fee=None,
        sharder_rewards=None,
        pending_pools=[miner_delegate_pool],
        active_pools=[miner_delegate_pool],
        deleting_pools=[miner_delegate_pool],
    ):

        return miner.update_miner_settings(
            self,
            miner_id,
            miner_url,
            delegate_client,
            service_charge,
            num_delegates,
            min_stake,
            max_stake,
            block_reward,
            service_charge_stat,
            users_fee,
            block_sharders_fee,
            sharder_rewards,
            pending_pools,
            active_pools,
            deleting_pools,
        )

    def allocation_min_lock(
        self,
        data_shards=AllocationConfig.DATA_SHARDS,
        parity_shards=AllocationConfig.PARITY_SHARDS,
        size=AllocationConfig.SIZE,
        preferred_blobbers=AllocationConfig.PREFERRED_BLOBBERS,
        write_price=AllocationConfig.WRITE_PRICE,
        read_price=AllocationConfig.READ_PRICE,
        max_challenge_completion_time=AllocationConfig.MAX_CHALLENGE_COMPLETION_TIME,
        expiration_date=time(),
    ):
        return allocation.allocation_min_lock(
            self,
            data_shards,
            parity_shards,
            size,
            preferred_blobbers,
            write_price,
            read_price,
            max_challenge_completion_time,
            expiration_date,
        )
