import argparse
import pathlib
import typing
import binascii
import unittest
from py_casper_tools.casper_tools import get_account_info, get_account_main_purse_uref, get_auction_info, get_state_root_hash

import pycspr #type: ignore
from pycspr.client import NodeClient #type: ignore
from pycspr.client import NodeConnectionInfo #type: ignore
from pycspr.crypto import KeyAlgorithm #type: ignore
from pycspr.types import PrivateKey #type: ignore
from pycspr.types import Deploy #type: ignore
from pycspr.types import PublicKey #type: ignore

from mainapp import casper_tools

account_key = ""

def test_get_account_info(client):
    print("begin test function")
    account_key = ""
    account_info = get_account_info(client, account_key)


    
def test_get_account_main_purse_uref(client):
    print("begin test function")
    account_key = ""
    state_root_hash = ""
    main_purse = get_account_main_purse_uref(client, account_key, state_root_hash)

    
def test_get_auction_info(client):
    print("begin test function")
    auction_data = get_auction_info(client)

    
def test_get_balance(client):
    print("begin test function")
    state_root_hash = get_state_root_hash(client)

    account_info = get_account_info(client, account_key)

    account_main_purse = get_account_main_purse_uref(client, account_key, get_state_root_hash(client))

    account_balance = client.queries.get_account_balance(account_main_purse, state_root_hash)

    
def test_get_block_transfers_by_hash(client):
    print("begin test function")

    
def test_get_block_transfers(client):
    print("begin test function")

    
def test_get_current_era(client):
    print("begin test function")

    
def test_get_block_at_era_switch(client):
    print("begin test function")

    
def test_get_last_block(client):
    print("begin test function")

    
def test_get_metrics(client):
    print("begin test function")

    
def test_get_node_peers(client):
    print("begin test function")

    
def test_get_rpc_schema(client):
    print("begin test function")

    
def test_get_state_root_hash(client):
    print("begin test function")

    
def test_get_status(client):
    print("begin test function")

    
def test_get_node_connection():
    print("begin test function")

# Create a new pycspr NodeClient instance
def test_get_node_connection(args: argparse.Namespace) -> pycspr.NodeClient:
    """Returns a pycspr client instance.

    """
    connection = pycspr.NodeConnectionInfo(
        host=args.node_host,
        port_rest=args.node_port_rest,
        port_rpc=args.node_port_rpc,
        port_sse=args.node_port_sse
    )

    return pycspr.NodeClient(connection)