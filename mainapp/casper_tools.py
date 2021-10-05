import argparse
import pathlib
import typing
import binascii

import pycspr
from pycspr.client import NodeClient
from pycspr.client import NodeConnectionInfo
from pycspr.crypto import KeyAlgorithm
from pycspr.types import PrivateKey
from pycspr.types import Deploy
from pycspr.types import PublicKey

# CLI argument parser.
args = argparse.ArgumentParser("Querying a node with pycspr.")

# CLI argument: path to public account key - defaults to casper default path, /etc/casper/validator_keys/public_key_hex.
args.add_argument(
    "--account-key-path",
    default=pathlib.Path("/etc/casper/validator_keys/public_key_hex"),
    dest="path_to_account_key",
    help="Path to a test user's public_key_hex file.",
    type=str,
    )

# CLI argument: host address of target node - defaults to localhost.
args.add_argument(
    "--node-address",
    default="localhost",
    dest="node_host",
    help="Host address of target node.",
    type=str,
    )

# CLI argument: Node API REST port - defaults to 8888.
args.add_argument(
    "--node-port-rest",
    default=8888,
    dest="node_port_rest",
    help="Node API REST port.  Typically 8888 on most nodes.",
    type=int,
    )

# CLI argument: Node API JSON-RPC port - defaults to 7777.
args.add_argument(
    "--node-port-rpc",
    default=7777,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
    )

# CLI argument: Node API SSE port - defaults to 9999.
args.add_argument(
    "--node-port-sse",
    default=9999,
    dest="node_port_sse",
    help="Node API SSE port.  Typically 9999 on most nodes.",
    type=int,
    )

args.add_argument(
    "--hash",
    dest="hash",
    help="Hash of block, account, deploy, etc.",
    type=str,
)

# CLI argument: Node endpoint/function requested
args.add_argument(
    "--get-info",
    required=True,
    dest="query",
    help="Requested Node Endpoint or Information.",
    choices=[
        'status', 
        'metrics', 
        'last_block', 
        'balance', 
        'current_era', 
        'auction_info', 
        'peers', 
        'rpc_schema', 
        'block_transfers', 
        'state_root_hash',
        'block_transfers_by_hash',
        'account_info',
        'switch_block'
        ],
    type=str,
)

# Queries a node for account information based on public key hex. Returns account hash, named keys stored, main purse uref and other metrics
def get_account_info(client, account_key):
    account_info: dict = client.queries.get_account_info(account_key.account_hash, get_state_root_hash(client))
    return account_info

# Queries a node to obtain an account's main purse uref.
def get_account_main_purse_uref(client, account_key, state_root_hash):
    account_main_purse: str = client.queries.get_account_main_purse_uref(account_key.account_key, state_root_hash)
    return account_main_purse

# Queries a node to obtain the current auction information including validator's delegation rates, delegators, stake amount and weight.
def get_auction_info(client):
    auction_info: dict = client.queries.get_auction_info()
    return auction_info

# Queries a node on the network for the balance of an account based on public key hex.
def get_balance(client, account_key):
    
    state_root_hash = get_state_root_hash(client)

    account_info = get_account_info(client, account_key)

    account_main_purse = get_account_main_purse_uref(client, account_key, get_state_root_hash(client))

    account_balance = client.queries.get_account_balance(account_main_purse, state_root_hash)

    return account_balance

# WIP: Working on incorporating the block hash identifier with the api call.
def get_block_transfers_by_hash(client, block_hash):
    block_transfers = client.queries.get_block_transfers(block_hash)
    return block_transfers

# Returns any transfers from the current block.
def get_block_transfers(client):
    current_block_transfers = client.queries.get_block_transfers()
    return current_block_transfers

# Queries a node for the current era's switch block info
def get_current_era(client):
    era: dict = client.queries.get_era_info()
    return era

#
def get_block_at_era_switch(client):
    block: dict = client.queries.get_block_at_era_switch()
    return block

# Queries a node for it's last added block
def get_last_block(client):
    block: dict = client.queries.get_block()
    return block

# Queries a node and returns a list of the reported system metrics for the node
def get_metrics(client):
    node_metrics: typing.List[str] = client.queries.get_node_metrics()
    return node_metrics

# Queries a node for it's current peer information
def get_node_peers(client):
    node_peers: typing.List[dict] = client.queries.get_node_peers()
    return node_peers

# Queries a node for the RPC schema
def get_rpc_schema(client):
    rpc_schema: typing.List[dict] = client.queries.get_rpc_schema()
    return rpc_schema

# Queries a node for the state root hash, the hash of the CURRENT state of the network
def get_state_root_hash(client):
    state_root_hash: bytes = client.queries.get_state_root_hash()
    return state_root_hash

# Query Node for latest downloaded block in the chain.
def get_status(client):
    node_status: typing.List[dict] = client.queries.get_node_status()
    return node_status

# Create a new pycspr NodeClient instance
def get_node_connection(args: argparse.Namespace) -> pycspr.NodeClient:
    """Returns a pycspr client instance.

    """
    connection = pycspr.NodeConnectionInfo(
        host=args.node_host,
        port_rest=args.node_port_rest,
        port_rpc=args.node_port_rpc,
        port_sse=args.node_port_sse
    )

    return pycspr.NodeClient(connection)



def main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set client.
    client = get_node_connection(args)

    # Set account key of test user.
    account_key = pycspr.parse_public_key(args.path_to_account_key)

    if args.query == "status":
        status = get_status(client)
        print(status)
    elif args.query == "metrics":
        metrics = get_metrics(client)
        print(metrics)
    elif args.query == "last_block":
        block = get_last_block(client)
        print(block)
    elif args.query == "balance":
        balance = get_balance(client, account_key) / 1000000000 # 9 decimal places for CSPR (called motes)
        print(balance)
    elif args.query == "current_era":
        request = get_current_era(client)
        print(request)
    elif args.query == "auction_info":
        auction = get_auction_info(client)
        bids = auction['auction_state']['bids']
        print(bids[0])
    elif args.query == "peers":
        peers = get_node_peers(client)
        print(peers)
    elif args.query == "rpc_schema":
        rpc_schema = get_rpc_schema(client)
        print(rpc_schema)
    elif args.query == "block_transfers":
        block_transfers = get_block_transfers(client)
        print(block_transfers)
    elif args.query == "block_transfers_by_hash":
        if args.hash:
            request = get_block_transfers_by_hash(client, block_hash=hash)
            print(request)
        else:
            print("Hash is required for this request.")
            exit(1)
    elif args.query == "state_root_hash":
        state_root_hash = binascii.hexlify(get_state_root_hash(client))
        state_root_hash_hex = state_root_hash.decode('utf-8')
        print(state_root_hash_hex)
    elif args.query == "account_info":
        account_info = get_account_info(client, account_key)
        print(account_info)
    elif args.query == "switch_block":
        era_switch_block = get_block_at_era_switch(client)
        print(era_switch_block)
    else: 
        print("ERROR: invalid CLI option. Please see python casper_tools.py -h for assistance.")

# Entry point.
if __name__ == '__main__':
    args = args.parse_args()
    main(args)