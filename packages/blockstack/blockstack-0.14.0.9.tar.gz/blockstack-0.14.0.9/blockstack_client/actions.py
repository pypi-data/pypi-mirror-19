#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Blockstack-client
    ~~~~~
    copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
    copyright: (c) 2016 by Blockstack.org

    This file is part of Blockstack-client.

    Blockstack-client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Blockstack-client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Blockstack-client. If not, see <http://www.gnu.org/licenses/>.
"""

"""
Every method that begins with `cli_` in this module
is matched to an action to be taken, based on the
CLI input.

Default options begin with `cli_`.  For exmample, "blockstack transfer ..."
will cause `cli_transfer(...)` to be called.

Advanced options begin with `cli_advanced_`.  For example, "blockstack wallet ..."
will cause `cli_advanced_wallet(...)` to be called.

The following conventions apply to `cli_` methods here:
* Each will always take a Namespace (from ArgumentParser.parse_known_args()) 
as its first argument.
* Each will return a dict with the requested information.  The key 'error'
will be set to indicate an error condition.

If you want to add a new command-line action, implement it here.  This
will make it available not only via the command-line, but also via the
local RPC interface and the test suite.
"""

import argparse
import sys
import json
import traceback
import os
import re
import errno
import pybitcoin
import virtualchain
import subprocess
from socket import error as socket_error
from time import sleep
from getpass import getpass
import time
import blockstack_zones
import blockstack_profiles
import requests
import base64
from decimal import Decimal

requests.packages.urllib3.disable_warnings()

import logging
logging.disable(logging.CRITICAL)

# Hack around absolute paths
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(current_dir + "/../")

sys.path.insert(0, parent_dir)

from blockstack_client import \
    delete_immutable, \
    delete_mutable, \
    get_all_names, \
    get_consensus_at, \
    get_immutable, \
    get_immutable_by_name, \
    get_mutable, \
    get_name_blockchain_record, \
    get_name_cost, \
    get_name_profile, \
    get_name_zonefile, \
    get_nameops_at, \
    get_names_in_namespace, \
    get_names_owned_by_address, \
    get_namespace_blockchain_record, \
    get_namespace_cost, \
    is_user_zonefile, \
    list_immutable_data_history, \
    list_update_history, \
    list_zonefile_history, \
    list_accounts, \
    get_account, \
    put_account, \
    delete_account, \
    lookup_snv, \
    put_immutable, \
    put_mutable

from blockstack_client.profile import profile_update, zonefile_data_replicate

from rpc import local_rpc_connect, local_rpc_status, local_rpc_stop, start_rpc_endpoint
import rpc as local_rpc
import config
from .config import WALLET_PATH, WALLET_PASSWORD_LENGTH, CONFIG_PATH, CONFIG_DIR, configure, FIRST_BLOCK_TIME_UTC, get_utxo_provider_client, set_advanced_mode, \
        APPROX_PREORDER_TX_LEN, APPROX_REGISTER_TX_LEN, APPROX_UPDATE_TX_LEN, APPROX_TRANSFER_TX_LEN, APPROX_REVOKE_TX_LEN, APPROX_RENEWAL_TX_LEN, configure_zonefile

from .storage import is_valid_hash, is_b40, get_drivers_for_url
from .user import add_user_zonefile_url, remove_user_zonefile_url

from pybitcoin import is_b58check_address

from binascii import hexlify

from .backend.blockchain import get_balance, is_address_usable, can_receive_name, get_tx_confirmations, get_tx_fee
from .backend.nameops import estimate_preorder_tx_fee, estimate_register_tx_fee, estimate_update_tx_fee, estimate_transfer_tx_fee, \
                            do_update, estimate_renewal_tx_fee

from .backend.queue import queuedb_remove, queuedb_find
from .backend.queue import extract_entry as queue_extract_entry

from .wallet import *
from .keys import *
from .utils import pretty_dump, print_result
from .proxy import *
from .client import analytics_event
from .app import app_register, app_unregister, app_get_wallet
from .scripts import UTXOException, is_name_valid
from .user import user_zonefile_urls, user_zonefile_data_pubkey, make_empty_user_zonefile 

log = config.get_logger()

def check_valid_name(fqu):
    """
    Verify that a name is valid.
    Return None on success
    Return an error string on error
    """
    rc = is_name_valid( fqu )
    if rc:
        return None

    # get a coherent reason why
    if '.' not in fqu:
        msg = 'The name specified is invalid.'
        msg += ' Names must end with a period followed by a valid TLD.'
        return msg

    if len(fqu.split('.')[0]) == 0:
        msg = 'The name specified is invalid.'
        msg += ' Names must be at least one character long, not including the TLD.'
        return msg

    if not is_b40( fqu.split('.')[0] ):
        msg = 'The name specified is invalid.'
        msg += ' Names may only contain lowercase alphanumeric characters,'
        msg += ' dashes, and underscores.'
        return msg

    return "The name is invalid"


def operation_sanity_check(fqu, payment_privkey_info, owner_privkey_info, config_path=CONFIG_PATH, transfer_address=None, proxy=None):
    """
    Any update, transfer, renew, or revoke operation
    should pass these tests:
    * name must be registered
    * name must be owned by the owner address in the wallet
    * the payment address must have enough BTC
    * the payment address can't have any pending transactions
    * if given, the transfer address must be suitable for receiving the name
    (i.e. it can't own too many names already).
    
    Return {'status': True} on success
    Return {'error': ...} on error
    """

    config_dir = os.path.dirname(config_path)
    wallet_path = os.path.join(config_dir, WALLET_FILENAME)

    if proxy is None:
        proxy = get_default_proxy(config_path)

    if not is_name_registered(fqu, proxy=proxy):
        return {'error': '%s is not registered yet.' % fqu}

    utxo_client = get_utxo_provider_client( config_path=config_path )
    payment_address, owner_address, data_address = get_addresses_from_file(wallet_path=wallet_path)

    if not is_name_owner(fqu, owner_address, proxy=proxy):
        return {'error': '%s is not in your possession.' % fqu}

    # get tx fee 
    if transfer_address is not None:
        tx_fee = estimate_transfer_tx_fee( fqu, payment_privkey_info, owner_address, utxo_client, owner_privkey_params=get_privkey_info_params(owner_privkey_info), config_path=config_path, include_dust=True )
        if tx_fee is None:
            # do our best 
            tx_fee = get_tx_fee( "00" * APPROX_TRANSFER_TX_LEN, config_path=config_path )

    else:
        tx_fee = estimate_update_tx_fee( fqu, payment_privkey_info, owner_address, utxo_client, owner_privkey_params=get_privkey_info_params(owner_privkey_info), config_path=config_path, include_dust=True )
        if tx_fee is None:
            # do our best
            tx_fee = get_tx_fee( "00" * APPROX_UPDATE_TX_LEN, config_path=config_path )

    if tx_fee is None:
        return {'error': 'Failed to get fee estimate'}

    balance = get_balance( payment_address, config_path=config_path )

    if balance < tx_fee:
        return {'error': 'Address %s doesn\'t have a sufficient balance (need %s).' % (payment_address, balance)}

    if not is_address_usable(payment_address, config_path=config_path):
        return {'error': 'Address %s has insufficiently confirmed transactions.  Wait and try later.' % payment_address}

    if transfer_address is not None:

        try:
            resp = is_b58check_address(str(transfer_address))
        except:
            return {'error': "Address %s is not a valid Bitcoin address." % transfer_address}

        if not can_receive_name(transfer_address, proxy=proxy):
            return {'error': "Address %s owns too many names already." % transfer_address}

    return {'status': True}


def get_total_registration_fees(name, payment_privkey_info, owner_privkey_info, proxy=None, config_path=CONFIG_PATH, payment_address=None):
    """
    Get all fees associated with registrations.
    Returned values are in satoshis.
    """
    try:
        data = get_name_cost(name, proxy=proxy)
    except Exception, e:
        log.exception(e)
        return {'error': 'Could not connect to server'}

    if 'error' in data:
        return {'error': 'Could not determine price of name: %s' % data['error']}

    insufficient_funds = False
    owner_address = None
    payment_address = None

    if payment_privkey_info is not None:
        payment_address = get_privkey_info_address(payment_privkey_info)

    if owner_privkey_info is not None:
        owner_address = get_privkey_info_address(owner_privkey_info)

    utxo_client = get_utxo_provider_client( config_path=config_path )
    
    # fee stimation: cost of name + cost of preorder transaction + cost of registration transaction + cost of update transaction
    reply = {}
    reply['name_price'] = data['satoshis']

    preorder_tx_fee = None
    register_tx_fee = None
    update_tx_fee = None

    try:
        preorder_tx_fee = estimate_preorder_tx_fee( name, data['satoshis'], payment_address, utxo_client, owner_privkey_params=get_privkey_info_params(owner_privkey_info), config_path=config_path, include_dust=True )
        if preorder_tx_fee is None:
            # do our best
            preorder_tx_fee = get_tx_fee( "00" * APPROX_PREORDER_TX_LEN, config_path=config_path )
            insufficient_funds = True
        else:
            preorder_tx_fee = int(preorder_tx_fee)

        register_tx_fee = estimate_register_tx_fee( name, payment_address, utxo_client, owner_privkey_params=get_privkey_info_params(owner_privkey_info), config_path=config_path, include_dust=True )
        if register_tx_fee is None:
            register_tx_fee = get_tx_fee( "00" * APPROX_REGISTER_TX_LEN, config_path=config_path )
            insufficient_funds = True
        else:
            register_tx_fee = int(register_tx_fee)

        update_tx_fee = estimate_update_tx_fee( name, payment_privkey_info, owner_address, utxo_client, \
                                                owner_privkey_params=get_privkey_info_params(owner_privkey_info), config_path=config_path, payment_address=payment_address, include_dust=True)
        if update_tx_fee is None:
            update_tx_fee = get_tx_fee( "00" * APPROX_UPDATE_TX_LEN, config_path=config_path )
            insufficient_funds = True
        else:
            update_tx_fee = int(update_tx_fee)

    except UTXOException, ue:
        log.error("Failed to query UTXO provider.")
        if os.environ.get("BLOCKSTACK_DEBUG", None) == "1":
            log.exception(ue)

        return {'error': 'Failed to query UTXO provider.  Please try again.'}

    reply['preorder_tx_fee'] = int(preorder_tx_fee)
    reply['register_tx_fee'] = int(register_tx_fee)
    reply['update_tx_fee'] = int(update_tx_fee)
    reply['total_estimated_cost'] = int(reply['name_price']) + reply['preorder_tx_fee'] + reply['register_tx_fee'] + reply['update_tx_fee']

    if insufficient_funds and payment_privkey_info is not None:
        reply['warnings'] = ["Insufficient funds; fees are rough estimates."]

    if payment_privkey_info is None:
        if not reply.has_key('warnings'):
            reply['warnings'] = []

        reply['warnings'].append("Wallet not accessed; fees are rough estimates.")

    return reply


def wallet_ensure_exists( config_dir=CONFIG_DIR, password=None, wallet_path=None ):
    """
    Ensure that the wallet exists and is initialized
    Return {'status': True} on success
    Return {'error': ...} on error
    """
    wallet_path = os.path.join(config_dir, WALLET_FILENAME)

    if not wallet_exists(config_dir=config_dir):
        res = initialize_wallet(wallet_path=wallet_path, password=password)
        if 'error' in res:
            return res

    return {'status': True}


def load_zonefile( fqu, zonefile_data, check_current=True ):
    """
    Load a zonefile from a string, which can be 
    either JSON or text.  Verify that it is
    well-formed and current.

    Return {'status': True, 'zonefile': the serialized zonefile data (as a string)} on success.
    Return {'error': ...} on error
    Return {'error': ..., 'identical': True, 'zonefile': serialized zonefile string} if the zonefile is identical
    """
    
    user_data = str(zonefile_data)
    user_zonefile = None
    try:
        user_data = json.loads(user_data)
    except:
        log.debug("Zonefile is not a serialized JSON string; try parsing as text")
        try:
            user_data = blockstack_zones.parse_zone_file(user_data)

            # force dict, not defaultdict
            tmp = {}
            tmp.update(user_data)
            user_data = tmp
        except Exception, e:
            if os.environ.get("BLOCKSTACK_TEST") == "1":
                log.exception(e)

            return {'error': 'Zonefile data is invalid.'}

    # is this a zonefile?
    try:
        user_zonefile = blockstack_zones.make_zone_file(user_data)
    except Exception, e:
        log.exception(e)
        log.error("Invalid zonefile")
        return {'error': 'Invalid zonefile\n%s' % traceback.format_exc()}

    # sanity checks...
    if not user_data.has_key('$origin') or user_data['$origin'] != fqu:
        log.error("Zonefile is missing or has invalid $origin")
        return {'error': 'Invalid $origin; must use your name'}

    if not user_data.has_key('$ttl'):
        log.error("Zonefile is missing a TTL")
        return {'error': 'Missing $ttl; please supply a positive integer'}

    if not is_user_zonefile(user_data):
        log.error("Zonefile is non-standard")
        return {'error': 'Zonefile is missing or has invalid URI and/or TXT records'}

    try:
        ttl = int(user_data['$ttl'])
        assert ttl >= 0
    except Exception, e:
        return {'error': 'Invalid $ttl; must be a positive integer'}

    if check_current and is_zonefile_current(fqu, user_data):
        msg = "Zonefile data is same as current zonefile; update not needed."
        log.error(msg)
        return {'error': msg, 'identical': True, 'zonefile': user_zonefile}

    return {'status': True, 'zonefile': user_zonefile}


def cli_configure( args, config_path=CONFIG_PATH ):
    """
    command: configure norpc
    help: Interactively configure the client
    """

    opts = configure( interactive=True, force=True, config_file=config_path )
    result = {}
    result['path'] = opts['blockstack-client']['path']
    return result


def cli_balance( args, config_path=CONFIG_PATH ):
    """
    command: balance norpc
    help: Get the account balance
    """

    config_dir = os.path.dirname(config_path)
    wallet_path = os.path.join(config_dir, WALLET_FILENAME)
    if not wallet_exists(config_dir=config_dir):
        res = initialize_wallet(wallet_path=wallet_path)
        if 'error' in res:
            return res

    result = {}
    addresses = []
    satoshis = 0
    satoshis, addresses = get_total_balance(wallet_path=wallet_path, config_path=config_path)

    # convert to BTC
    btc = float(Decimal(satoshis / 1e8))

    for address_info in addresses:
        address_info['bitcoin'] = float(Decimal(address_info['balance'] / 1e8))
        address_info['satoshis'] = address_info['balance']
        del address_info['balance']

    result = {
        'total_balance': {
            'satoshis': int(satoshis),
            'bitcoin': btc
        },
        'addresses': addresses
    }

    return result


def cli_price( args, config_path=CONFIG_PATH, proxy=None, password=None):
    """
    command: price
    help: Get the price of a name
    arg: name (str) "Name to query"
    """

    if proxy is None:
        proxy = get_default_proxy()

    fqu = str(args.name)
    error = check_valid_name(fqu)
    config_dir = os.path.dirname(config_path)
    wallet_path = os.path.join(config_dir, WALLET_FILENAME)

    payment_privkey_info = None
    owner_privkey_info = None
    payment_address = None
    owner_address = None

    if error:
        return {'error': error}

    payment_address, owner_address, data_pubkey = get_addresses_from_file(config_dir=config_dir, wallet_path=wallet_path)

    if local_rpc_status(config_dir=config_dir):
        try:
            wallet_keys = get_wallet_keys( config_path, password )
            if 'error' in wallet_keys:
                return wallet_keys

            payment_privkey_info = wallet_keys['payment_privkey']
            owner_privkey_info = wallet_keys['owner_privkey']
        
        except (OSError, IOError), e:
            # backend is not running; estimate with addresses
            if os.environ.get("BLOCKSTACK_DEBUG") == "1":
                log.exception(e)

            pass

    # must be available 
    try:
        blockchain_record = get_name_blockchain_record(fqu)
    except socket_error:
        return {'error': 'Error connecting to server.'}

    if 'owner_address' in blockchain_record:
        return {'error': 'Name already registered.'}

    fees = get_total_registration_fees( fqu, payment_privkey_info, owner_privkey_info, proxy=proxy, config_path=config_path, payment_address=payment_address )
    analytics_event( "Name price", {} )

    if 'error' in fees:
        return fees

    # convert to BTC
    btc_keys = ['preorder_tx_fee', 'register_tx_fee', 'update_tx_fee', 'total_estimated_cost', 'name_price']
    for k in btc_keys:
        v = {
            "satoshis": "%s" % fees[k],
            "btc": "%s" % float(Decimal(fees[k] * 1e-8))
        }
        fees[k] = v

    return fees


def cli_deposit( args, config_path=CONFIG_PATH ):
    """
    command: deposit norpc
    help: Display the address with which to receive bitcoins
    """

    config_dir = os.path.dirname(config_path)
    wallet_path = os.path.join(config_dir, WALLET_FILENAME)
    if not os.path.exists(wallet_path):
        res = initialize_wallet(wallet_path=wallet_path)
        if 'error' in res:
            return res

    result = {}
    result['message'] = 'Send bitcoins to the address specified.'
    result['address'], owner_address, data_address = get_addresses_from_file(wallet_path=wallet_path)
    return result


def cli_import( args, config_path=CONFIG_PATH ):
    """
    command: import norpc
    help: Display the address with which to receive names
    """

    config_dir = os.path.dirname(config_path)
    wallet_path = os.path.join(config_dir, WALLET_FILENAME)
    if not os.path.exists(wallet_path):
        res = initialize_wallet(wallet_path=wallet_path)
        if 'error' in res:
            return res

    result = {}
    result['message'] = 'Send the name you want to receive to the'
    result['message'] += ' address specified.'
    payment_address, result['address'], data_address = get_addresses_from_file(wallet_path=wallet_path)

    return result


def cli_names( args, config_path=CONFIG_DIR ):
    """
    command: names norpc
    help: Display the names owned by local addresses
    """
    result = {}

    config_dir = os.path.dirname(config_path)
    wallet_path = os.path.join(config_dir, WALLET_FILENAME)
    if not os.path.exists(wallet_path):
        res = initialize_wallet(wallet_path=wallet_path)
        if 'error' in res:
            return res

    result['names_owned'] = get_all_names_owned(wallet_path)
    result['addresses'] = get_owner_addresses_and_names(wallet_path)

    return result


def get_server_info( args, config_path=config.CONFIG_PATH, get_local_info=False ):
    """
    Get information about the running server,
    and any pending operations.
    """
    
    config_dir = os.path.dirname(config_path)
    conf = config.get_config(config_path)

    resp = getinfo()
    result = {}

    result['cli_version'] = config.VERSION
    result['advanced_mode'] = conf['advanced_mode']

    if 'error' in resp:
        result['server_alive'] = False
        result['server_error'] = resp['error']

    else:
        result['server_alive'] = True

        if 'server_host' in resp:
            result['server_host'] = resp['server_host']
        else:
            result['server_host'] = conf['server']

        if 'server_port' in resp:
            result['server_port'] = resp['server_port']
        else:
            result['server_port'] = int(conf['port'])

        if 'server_version' in resp:
            result['server_version'] = resp['server_version']
        elif 'blockstack_version' in resp:
            result['server_version'] = resp['blockstack_version']
        elif 'blockstore_version' in resp:
            result['server_version'] = resp['blockstore_version']
        else:
            raise Exception("Missing server version")

        if 'last_block_processed' in resp:
            result['last_block_processed'] = resp['last_block_processed']
        elif 'last_block' in resp:
            result['last_block_processed'] = resp['last_block']
        elif 'blocks' in resp:
            result['last_block_processed'] = resp['blocks']
        else:
            raise Exception("Missing height of block last processed")

        if 'last_block_seen' in resp:
            result['last_block_seen'] = resp['last_block_seen']
        elif 'blockchain_blocks' in resp:
            result['last_block_seen'] = resp['blockchain_blocks']
        elif 'bitcoind_blocks' in resp:
            result['last_block_seen'] = resp['bitcoind_blocks']
        else:
            raise Exception("Missing height of last block seen")

        try:
            result['consensus_hash'] = resp['consensus']
        except:
            raise Exception("Missing consensus hash")

        if get_local_info:
            # get state of pending names
            res = wallet_ensure_exists(config_dir)
            if 'error' in res:
                return res

            res = start_rpc_endpoint(config_dir)
            if 'error' in res:
                return res 

            rpc = local_rpc_connect(config_dir=config_dir)

            if rpc is not None:

                current_state = json.loads(rpc.backend_state())

                queue_types = {
                    "preorder": [],
                    "register": [],
                    "update": [],
                    "transfer": []
                }

                def format_new_entry(entry):
                    """
                    Determine data to display
                    """
                    new_entry = {}
                    new_entry['name'] = entry['fqu']
                    confirmations = get_tx_confirmations(entry['tx_hash'], config_path=config_path)
                    if confirmations is None:
                        confirmations = 0
                    new_entry['confirmations'] = confirmations
                    new_entry['tx_hash'] = entry['tx_hash']
                    return new_entry

                def format_queue_display(preorder_queue,
                                         register_queue):

                    """
                    Omit duplicates
                    """
                    for entry in register_queue:
                        name = entry['name']
                        for check_entry in preorder_queue:
                            if check_entry['name'] == name:
                                preorder_queue.remove(check_entry)

                for entry in current_state:
                    if entry['type'] not in queue_types.keys():
                        log.error("Unknown entry type '%s'" % entry['type'])
                        continue

                    queue_types[ entry['type'] ].append( format_new_entry(entry) )

                format_queue_display(queue_types['preorder'], queue_types['register'])

                for queue_type in queue_types.keys():
                    if len(queue_types[queue_type]) == 0:
                        del queue_types[queue_type]

                if len(queue_types) > 0:
                    result['queue'] = queue_types

    return result


def cli_info( args, config_path=CONFIG_PATH ):
    """
    command: info norpc
    help: Get details about pending name commands
    """
    return get_server_info( args, config_path=config_path, get_local_info=True )


def cli_ping( args, config_path=CONFIG_PATH ):
    """
    command: ping
    help: Check server status and get server details
    """
    return get_server_info( args, config_path=config_path )


def cli_lookup( args, config_path=CONFIG_PATH ):
    """
    command: lookup
    help: Get the zone file and profile for a particular name
    arg: name (str) "The name to look up"
    """
    data = {}

    blockchain_record = None
    fqu = str(args.name)

    error = check_valid_name(fqu)
    if error:
        return {'error': error}

    try:
        blockchain_record = get_name_blockchain_record(fqu)
    except socket_error:
        return {'error': 'Error connecting to server.'}
 

    if 'error' in blockchain_record:
        return blockchain_record

    if 'value_hash' not in blockchain_record:
        return {'error': '%s has no profile' % fqu}

    if blockchain_record.has_key('revoked') and blockchain_record['revoked']:
        return {'error': 'Name is revoked.  Use get_name_blockchain_record for details.'}
    try:
        user_profile, user_zonefile = get_name_profile(str(args.name), name_record=blockchain_record, include_raw_zonefile=True)
        if isinstance(user_zonefile, dict) and 'error' in user_zonefile:
            return user_zonefile

        data['profile'] = user_profile
        data['zonefile'] = user_zonefile['raw_zonefile']
    except Exception, e:
        log.exception(e)
        return {'error': 'Failed to look up name\n%s' % traceback.format_exc()}

    result = data
    analytics_event( "Name lookup", {} )
    return result 


def cli_whois( args, config_path=CONFIG_PATH ):
    """
    command: whois
    help: Look up the blockchain info for a name
    arg: name (str) "The name to look up"
    """
    result = {}

    record = None
    fqu = str(args.name)

    error = check_valid_name(fqu)
    if error:
        return {'error': error}

    try:
        record = get_name_blockchain_record(fqu)
    except socket_error:
        exit_with_error("Error connecting to server.")

    if 'error' in record:
        return record

    else:
        if record.has_key('revoked') and record['revoked']:
            return {'error': 'Name is revoked.  Use get_name_blockchain_record for details.'}

        history = record.get('history', {})
        try:
            assert type(history) == dict

            for k in history.keys():
                # must be ints 
                i = int(k)

        except:
            return {'error': 'Invalid record data returned'}

        update_heights = [int(k) for k in history.keys()]
        update_heights.sort()

        result['block_preordered_at'] = record['preorder_block_number']
        result['block_renewed_at'] = record['last_renewed']
        result['last_transaction_id'] = record['txid']
        result['owner_address'] = record['address']
        result['owner_script'] = record['sender']

        if len(update_heights) > 0:
            result['last_transaction_height'] = update_heights[-1]

        if not record.has_key('value_hash') or record['value_hash'] in [None, "null", ""]:
            result['has_zonefile'] = False
        else:
            result['has_zonefile'] = True
            result['zonefile_hash'] = record['value_hash']

        if record.has_key('expire_block'):
            result['expire_block'] = record['expire_block']

    analytics_event( "Whois", {} )
    return result


def get_wallet_with_backoff( config_path ):
    """
    Get the wallet, but keep trying
    in the case of a ECONNREFUSED
    (i.e. the API daemon could still be initializing)

    Return the wallet keys on success (as a dict)
    return {'error': ...} on error
    """

    wallet_keys = None
    for i in xrange(0, 3):
        try:
            wallet_keys = get_wallet( config_path=config_path )
            return wallet_keys
        except (IOError, OSError), se:
            if se.errno == errno.ECONNREFUSED:
                # still spinning up
                time.sleep(i+1)
                continue
            else:
                raise

    if i == 3:
        log.error("Failed to get_wallet")
        wallet_keys = {'error': 'Failed to connect to API daemon'}

    return wallet_keys


def get_wallet_keys( config_path, password ):
    """
    Load up the wallet keys
    Return the dict with the keys on success
    Return {'error': ...} on failure
    """
    
    config_dir = os.path.dirname(config_path)
    wallet_path = os.path.join(config_dir, WALLET_FILENAME)
    if not os.path.exists(wallet_path):
        res = initialize_wallet(wallet_path=wallet_path)
        if 'error' in res:
            return res

    if not is_wallet_unlocked(config_dir=config_dir):
        log.debug("unlocking wallet (%s)" % config_dir)
        res = unlock_wallet(config_dir=config_dir, password=password)
        if 'error' in res:
            log.error("unlock_wallet: %s" % res['error'])
            return res

    return get_wallet_with_backoff( config_path )


def prompt_invalid_zonefile():
    """
    Prompt the user whether or not to replicate
    an invalid zonefile
    """
    warning_str = "\n"
    warning_str += "WARNING!  This zone file data does not look like a zone file.\n"
    warning_str += "If you proceed to use this data, no one will be able to look\n"
    warning_str += "up your profile.\n"
    warning_str += "\n"
    warning_str += "Proceed? (Y/n): "
    proceed = raw_input(warning_str)
    return proceed.lower() in ['y']


def is_valid_path( path ):
    """
    Is the given string a valid path?
    """
    if type(path) not in [str]:
        return False

    if '\x00' in path:
        return False

    return True


def cli_register( args, config_path=CONFIG_PATH, interactive=True, password=None, proxy=None ):
    """
    command: register norpc
    help: Register a name 
    arg: name (str) "The name to register"
    """

    if proxy is None:
        proxy = get_default_proxy(config_path)

    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir, password=password)
    if 'error' in res:
        return res

    result = {}
    fqu = str(args.name)
    error = check_valid_name(fqu)
    if error: 
        return {'error': error}

    if is_name_registered(fqu, proxy=proxy):
        return {'error': '%s is already registered.' % fqu}

    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    owner_privkey_info = wallet_keys['owner_privkey']
    payment_privkey_info = wallet_keys['payment_privkey']

    owner_address = get_privkey_info_address( owner_privkey_info )
    payment_address = get_privkey_info_address( payment_privkey_info )

    fees = get_total_registration_fees(fqu, payment_privkey_info, owner_privkey_info, proxy=proxy, config_path=config_path)
    if 'error' in fees:
        return fees

    if interactive:
        try:
            cost = fees['total_estimated_cost']
            input_prompt = "Registering %s will cost %s BTC.\n" % (fqu, float(cost)/(10**8))
            input_prompt+= "The entire process takes 30 confirmations, or about 5 hours.\n"
            input_prompt+= "You need to have Internet access during this time period, so\n"
            input_prompt+= "this program can send the right transactions at the right\n"
            input_prompt+= "times.\n\n"
            input_prompt += "Continue? (Y/n): "
            user_input = raw_input(input_prompt)
            user_input = user_input.lower()

            if user_input.lower() != 'y':
                print "Not registering."
                exit(0)
        except KeyboardInterrupt:
            print "\nExiting."
            exit(0)

    balance = get_balance( payment_address, config_path=config_path )
    if balance < fees['total_estimated_cost']:
        msg = "Address %s doesn't have enough balance (need %s, have %s)." % (payment_address, fees['total_estimated_cost'], balance)
        return {'error': msg}

    if not can_receive_name(owner_address, proxy=proxy):
        msg = "Address %s owns too many names already." % owner_address
        return {'error': msg}

    if not is_address_usable(payment_address, config_path=config_path):
        msg = "Address %s has insufficiently confirmed transactions." % payment_address
        msg += " Wait and try later."
        return {'error': msg}

    rpc = local_rpc_connect( config_dir=config_dir )

    try:
        resp = rpc.backend_preorder(fqu)
    except:
        return {'error': 'Error talking to server, try again.'}

    if 'success' in resp and resp['success']:
        result = resp
    else:
        if 'error' in resp:
            log.debug("RPC error: %s" % resp['error'])
            return resp

        if 'message' in resp:
            return {'error': resp['message']}

    analytics_event( "Register name", {"total_estimated_cost": fees['total_estimated_cost']} )
    return result


def cli_update( args, config_path=CONFIG_PATH, password=None, interactive=True, proxy=None, nonstandard=False ):
    """
    command: update norpc
    help: Set the zone file for a name
    arg: name (str) "The name to update"
    opt: data (str) "A zone file string, or a path to a file with the data."
    opt: nonstandard (str) "If true, then do not validate or parse the zonefile."
    """

    if not interactive and (not hasattr(args, "data") or args.data is None):
        return {'error': 'Zone file data required in non-interactive mode'}
        
    if proxy is None:
        proxy = get_default_proxy()

    if hasattr(args, 'nonstandard') and not nonstandard:
        if args.nonstandard is not None and args.nonstandard.lower() in ['yes', '1', 'true']:
            nonstandard = True

    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir, password=password)
    if 'error' in res:
        return res

    fqu = str(args.name)
    zonefile_data = None
    if hasattr(args, "data") and args.data is not None:
        zonefile_data = str(args.data)

    error = check_valid_name(fqu)
    if error:
        return {'error': error}

    # is this a path?
    if zonefile_data is not None and is_valid_path(zonefile_data) and os.path.exists(zonefile_data):
        try:
            with open(zonefile_data) as f:
                zonefile_data = f.read()
        except:
            return {'error': 'Failed to read "%s"' % zonefile_data}
    
    # load wallet
    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    # fetch remotely?
    if zonefile_data is None:
        zonefile_data_res = get_name_zonefile( fqu, proxy=proxy, wallet_keys=wallet_keys, raw_zonefile=True )
        if zonefile_data_res is None:
            zonefile_data_res = {'error': 'No zonefile'}
        
        if 'error' in zonefile_data_res:
            log.warning("Failed to fetch zonefile: %s" % zonefile_data_res['error'])

        else:
            zonefile_data = zonefile_data_res['zonefile']

    # load zonefile, if given 
    user_data_txt = None
    user_data_hash = None
    user_zonefile_dict = {}

    user_data_res = load_zonefile( fqu, zonefile_data )
    if 'error' in user_data_res:
        if 'identical' in user_data_res.keys():
            return {'error': 'Zonefile matches the current name hash; not updating.'}

        #  not a well-formed zonefile (but maybe that's okay! ask the user)
        if interactive:
            if zonefile_data is not None:
                # something invalid here.  prompt overwrite
                proceed = prompt_invalid_zonefile()
                if not proceed:
                    return {'error': "Zone file not updated (reason: %s)" % user_data_res['error']}

        else:
            if zonefile_data is None or nonstandard:
                log.warning("Using non-zonefile data")
            else:
                return {'error': 'Zone file not updated (invalid)'}

        user_data_txt = zonefile_data
        if zonefile_data is not None:
            user_data_hash = storage.get_zonefile_data_hash(zonefile_data) 

    else:
        user_data_txt = user_data_res['zonefile']
        user_data_hash = storage.get_zonefile_data_hash( user_data_res['zonefile'] )
        user_zonefile_dict = blockstack_zones.parse_zone_file( user_data_res['zonefile'] )

    # open the zonefile editor
    data_pubkey = wallet_keys['data_pubkey']

    '''
    if interactive:
        new_zonefile = configure_zonefile( fqu, user_zonefile_dict, data_pubkey=data_pubkey )
        if new_zonefile is None:
            # zonefile did not change; nothing to do
            return {'error': 'Zonefile did not change.  No update sent.'}
    '''

    payment_privkey_info = wallet_keys['payment_privkey']
    owner_privkey_info = wallet_keys['owner_privkey']

    res = operation_sanity_check(fqu, payment_privkey_info, owner_privkey_info, config_path=config_path)
    if 'error' in res:
        return res

    rpc = local_rpc_connect(config_dir=config_dir)

    try:
        resp = rpc.backend_update(fqu, base64.b64encode(user_data_txt), None, user_data_hash)
    except Exception, e:
        log.exception(e)
        return {'error': 'Error talking to server, try again.'}

    if 'success' in resp and resp['success']:
        result = resp
    else:
        if 'error' in resp:
            log.error("Backend failed to queue update: %s" % resp['error'])
            return resp

        if 'message' in resp:
            log.error("Backend reports error: %s" % resp['message'])
            return {'error': resp['message']}

    analytics_event( "Update name", {} )
    return result


def cli_transfer( args, config_path=CONFIG_PATH, password=None ):
    """
    command: transfer norpc
    help: Transfer a name to a new address
    arg: name (str) "The name to transfer"
    arg: address (str) "The address to receive the name"
    """

    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir, password=password)
    if 'error' in res:
        return res

    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    fqu = str(args.name)
    error = check_valid_name(fqu)
    if error:
        return {'error': error}

    # load wallet
    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    payment_privkey_info = wallet_keys['payment_privkey']
    owner_privkey_info = wallet_keys['owner_privkey']

    transfer_address = str(args.address)
    res = operation_sanity_check(fqu, payment_privkey_info, owner_privkey_info, transfer_address=transfer_address, config_path=config_path)
    if 'error' in res:
        return res

    rpc = local_rpc_connect(config_dir=config_dir)

    try:
        resp = rpc.backend_transfer(fqu, transfer_address)
    except:
        return {'error': 'Error talking to server, try again.'}

    if 'success' in resp and resp['success']:
        result = resp
    else:
        if 'error' in resp:
            return resp

        if 'message' in resp:
            return {'error': resp['message']}

    analytics_event( "Transfer name", {} )
    return result


def cli_renew( args, config_path=CONFIG_PATH, interactive=True, password=None, proxy=None ):
    """
    command: renew norpc
    help: Renew a name 
    arg: name (str) "The name to renew"
    """

    if proxy is None:
        proxy = get_default_proxy(config_path)

    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir, password=password)
    if 'error' in res:
        return res


    result = {}
    fqu = str(args.name)
    error = check_valid_name(fqu)
    if error: 
        return {'error': error}

    if not is_name_registered(fqu, proxy=proxy):
        return {'error': '%s does not exist.' % fqu}

    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    owner_privkey_info = wallet_keys['owner_privkey']
    payment_privkey_info = wallet_keys['payment_privkey']

    owner_address = get_privkey_info_address(owner_privkey_info)
    payment_address = get_privkey_info_address(payment_privkey_info)

    if not is_name_owner(fqu, owner_address, proxy=proxy):
        return {'error': '%s is not in your possession.' % fqu}

    # estimate renewal fees 
    try:
        renewal_fee = get_name_cost(fqu, proxy=proxy)
    except Exception, e:
        log.exception(e)
        return {'error': 'Could not connect to server'}

    if 'error' in renewal_fee:
        return {'error': 'Could not determine price of name: %s' % renewal_fee['error']}

    utxo_client = get_utxo_provider_client( config_path=config_path )
    
    # fee stimation: cost of name + cost of renewal transaction
    name_price = renewal_fee['satoshis']
    renewal_tx_fee = estimate_renewal_tx_fee( fqu, name_price, payment_privkey_info, owner_privkey_info, utxo_client, config_path=config_path )
    if renewal_tx_fee is None:
        return {'error': 'Failed to estimate fee'}

    cost = name_price + renewal_tx_fee

    if interactive:
        try:
            cost = name_price + renewal_tx_fee
            input_prompt = "Renewing %s will cost %s BTC." % (fqu, float(cost)/(10**8))
            input_prompt += " Continue? (y/n): "
            user_input = raw_input(input_prompt)
            user_input = user_input.lower()

            if user_input != 'y':
                print "Not renewing."
                exit(0)
        except KeyboardInterrupt:
            print "\nExiting."
            exit(0)

    balance = get_balance( payment_address, config_path=config_path )
    if balance < cost:
        msg = "Address %s doesn't have enough balance (need %s)." % (payment_address, balance)
        return {'error': msg}

    if not is_address_usable(payment_address, config_path=config_path):
        msg = "Address %s has insufficiently confirmed transactions." % payment_address
        msg += " Wait and try later."
        return {'error': msg}

    rpc = local_rpc_connect( config_dir=config_dir )

    try:
        resp = rpc.backend_renew(fqu, name_price)
    except:
        return {'error': 'Error talking to server, try again.'}

    if 'success' in resp and resp['success']:
        result = resp
    else:
        if 'error' in resp:
            log.debug("RPC error: %s" % resp['error'])
            return resp

        if 'message' in resp:
            return {'error': resp['message']}

    analytics_event( "Renew name", {'total_estimated_cost': cost} )
    return result


def cli_revoke( args, config_path=CONFIG_PATH, interactive=True, password=None, proxy=None ):
    """
    command: revoke norpc
    help: Revoke a name 
    arg: name (str) "The name to revoke"
    """

    if proxy is None:
        proxy = get_default_proxy(config_path)

    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir, password=password)
    if 'error' in res:
        return res

    result = {}
    fqu = str(args.name)
    error = check_valid_name(fqu)
    if error: 
        return {'error': error}

    if not is_name_registered(fqu, proxy=proxy):
        return {'error': '%s does not exist.' % fqu}

    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    owner_privkey_info = wallet_keys['owner_privkey']
    payment_privkey_info = wallet_keys['payment_privkey']
    owner_address = get_privkey_info_address( owner_privkey_info )
    payment_address = get_privkey_info_address( payment_privkey_info )

    res = operation_sanity_check(fqu, payment_privkey_info, owner_privkey_info, config_path=config_path)
    if 'error' in res:
        return res

    if interactive:
        try:
            input_prompt = "==============================\n"
            input_prompt+= "WARNING: THIS CANNOT BE UNDONE\n"
            input_prompt+= "==============================\n"
            input_prompt+= " Are you sure? (y/n): "
            user_input = raw_input(input_prompt)
            user_input = user_input.lower()

            if user_input != 'y':
                print "Not revoking."
                exit(0)

        except KeyboardInterrupt:
            print "\nExiting."
            exit(0)

    rpc = local_rpc_connect( config_dir=config_dir )

    try:
        resp = rpc.backend_revoke(fqu)
    except:
        return {'error': 'Error talking to server, try again.'}

    if 'success' in resp and resp['success']:
        result = resp
    else:
        if 'error' in resp:
            log.debug("RPC error: %s" % resp['error'])
            return resp

        if 'message' in resp:
            return {'error': resp['message']}

    analytics_event( "Revoke name", {} )
    return result



def cli_migrate( args, config_path=CONFIG_PATH, password=None, proxy=None, interactive=True, force=False ):
    """
    command: migrate norpc
    help: Migrate a profile to the latest profile format
    arg: name (str) "The name to migrate"
    opt: txid (str) "The transaction ID of a previously-sent but failed migration"
    """

    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir)
    if 'error' in res:
        return res

    if proxy is None:
        proxy = get_default_proxy(config_path=config_path)

    fqu = str(args.name)
    error = check_valid_name(fqu)
    if error:
        return {'error': error}

    res = start_rpc_endpoint(config_dir, password=password)
    if 'error' in res:
        return res

    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    owner_privkey_info = wallet_keys['owner_privkey']
    payment_privkey_info = wallet_keys['payment_privkey']

    res = operation_sanity_check(fqu, payment_privkey_info, owner_privkey_info, config_path=config_path)
    if 'error' in res:
        return res

    user_zonefile = get_name_zonefile( fqu, proxy=proxy, wallet_keys=wallet_keys, raw_zonefile=True, include_name_record=True )
    if user_zonefile is not None and 'error' not in user_zonefile:

        name_rec = user_zonefile['name_record']
        user_zonefile_txt = user_zonefile['zonefile']
        user_zonefile_hash = storage.get_zonefile_data_hash( user_zonefile_txt )
        user_zonefile = None
        legacy = False
        nonstandard = False

        # try to parse
        try:
            user_zonefile = blockstack_zones.parse_zone_file( user_zonefile_txt )
            legacy = blockstack_profiles.is_profile_in_legacy_format( user_zonefile )
        except:
            log.warning("Non-standard zonefile %s" % user_zonefile_hash)
            nonstandard = True

        current = ('value_hash' in name_rec and name_rec['value_hash'] == user_zonefile_hash)

        if nonstandard and not legacy:
            # maybe we're trying to reset the profile?
            if interactive and not force:
                msg = ""
                msg += "WARNING!  Non-standard zonefile detected."
                msg += "If you proceed, your zonefile will be reset"
                msg += "and you will have to re-build your profile."
                msg += ""
                msg += "Proceed? (Y/n): "
                proceed_str = raw_input(msg)
                proceed = (proceed_str.lower() in ['y'])
                if not proceed:
                    return {'error': 'Non-standard zonefile'}

            elif not force:
                return {'error': 'Non-standard zonefile'}

        # is current and either standard or legacy?
        elif not legacy and not force:
            if current:
                msg = "Zonefile data is same as current zonefile; update not needed."
                return {'error': msg}

            else:
                # maybe this is intentional (like fixing a corrupt zonefile)
                msg = "Not a legacy profile; cannot migrate."
                return {'error': msg}

    rpc = local_rpc_connect(config_dir=config_dir)

    try:
        resp = rpc.backend_migrate(fqu)
    except Exception, e:
        log.exception(e)
        return {'error': 'Error talking to server, try again.'}

    if 'success' in resp and resp['success']:
        result = resp
    else:
        if 'error' in resp:
            return resp

        if 'message' in resp:
            return {'error': resp['message']}

    analytics_event( "Migrate name", {} )
    return result


def cli_set_advanced_mode( args, config_path=CONFIG_PATH ):
    """
    command: set_advanced_mode norpc
    help: Enable advanced commands
    arg: status (str) "On or Off."
    """

    status = str(args.status).lower()
    if status not in ['on', 'off']:
        return {'error': 'Invalid option; please use "on" or "off"'}

    if status == 'on':
        set_advanced_mode(True, config_path=config_path)
    else:
        set_advanced_mode(False, config_path=config_path)

    return {'status': True}


def cli_advanced_import_wallet( args, config_path=CONFIG_PATH, password=None, force=False ):
    """
    command: import_wallet norpc
    help: Set the payment, owner, and (optionally) data private keys for the wallet.
    arg: payment_privkey (str) "Payment private key"
    arg: owner_privkey (str) "Name owner private key"
    opt: data_privkey (str) "Data-signing private key"
    """
    config_dir = os.path.dirname(config_path)
    wallet_path = os.path.join(config_dir, WALLET_FILENAME)
    if force and os.path.exists(wallet_path):
        # overwrite
        os.unlink(wallet_path)

    if not os.path.exists(wallet_path):
        if password is None:

            while True:
                res = make_wallet_password(password)
                if 'error' in res and password is None:
                    print res['error']
                    continue

                elif password is not None:
                    return res

                else:
                    password = res['password']
                    break

        data_privkey = args.data_privkey
        if data_privkey is None or len(data_privkey) == 0:
            # generate one, since it's an optional argument
            data_privkey = virtualchain.BitcoinPrivateKey().to_wif()

        # make absolutely certain that these are valid keys 
        try:
            assert len(args.payment_privkey) > 0
            assert len(args.owner_privkey) > 0
            virtualchain.BitcoinPrivateKey(args.payment_privkey)
            virtualchain.BitcoinPrivateKey(args.owner_privkey)
            virtualchain.BitcoinPrivateKey(data_privkey)
        except:
            return {'error': 'Invalid payment or owner private key'}

        data = make_wallet( password, payment_privkey=args.payment_privkey, owner_privkey=args.owner_privkey, data_privkey=data_privkey, config_path=config_path ) 
        if 'error' in data:
            return data

        else:
            write_wallet( data, path=wallet_path )

            # update RPC daemon if we're running
            if local_rpc_status(config_dir=config_dir):
                local_rpc_stop(config_dir=config_dir)

                res = start_rpc_endpoint(config_dir, password=password)
                if 'error' in res:
                    return res

            return {'status': True}

    else:
        return {'error': 'Wallet already exists!', 'message': 'Back up or remove current wallet first: %s' % wallet_path}



def cli_advanced_list_accounts( args, proxy=None, config_path=CONFIG_PATH, password=None ):
    """
    command: list_accounts
    help: List the set of accounts associated with a name.
    arg: name (str) "The name to query."
    """ 

    result = {}
    config_dir = os.path.dirname(config_path)
    if proxy is None:
        proxy = get_default_proxy(config_path=config_path)

    result = list_accounts( args.name, proxy=proxy )
    if 'error' not in result:
        analytics_event( "List accounts", {} )

    return result
   

def cli_advanced_get_account( args, proxy=None, config_path=CONFIG_PATH, password=None ):
    """
    command: get_account
    help: Get a particular account from a name.
    arg: name (str) "The name to query."
    arg: service (str) "The service for which this account was created."
    arg: identifier (str) "The name of the account."
    """

    result = {}
    config_dir = os.path.dirname(config_path)
    if not is_name_valid(args.name) or len(args.service) == 0 or len(args.identifier) == 0:
        return {'error': 'Invalid name or identifier'}

    if proxy is None:
        proxy = get_default_proxy(config_path=config_path)

    result = get_account( args.name, args.service, args.identifier, proxy=proxy )
    if 'error' not in result:
        analytics_event( "Get account", {} )

    return result
    

def cli_advanced_put_account( args, proxy=None, config_path=CONFIG_PATH, password=None, required_drivers=None ):
    """
    command: put_account norpc
    help: Set a particular account's details.  If the account already exists, it will be overwritten.
    arg: name (str) "The name to query."
    arg: service (str) "The service this account is for."
    arg: identifier (str) "The name of the account."
    arg: content_url (str) "The URL that points to external contact data."
    opt: extra_data (str) "A comma-separated list of 'name1=value1,name2=value2,name3=value3...' with any extra account information you need in the account."
    """

    result = {}
    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir, password=password)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir, password=password)
    if 'error' in res:
        return res


    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys
    
    if proxy is None:
        proxy = get_default_proxy(config_path=config_path)

    if not is_name_valid(args.name):
        return {'error': 'Invalid name'}

    if len(args.service) == 0 or len(args.identifier) == 0 or len(args.content_url) == 0:
        return {'error': 'Invalid data'}

    # parse extra data 
    extra_data = {}
    if hasattr(args, "extra_data") and args.extra_data is not None:
        extra_data_str = str(args.extra_data)
        if len(extra_data_str) > 0:
            extra_data_pairs = extra_data_str.split(",")
            for p in extra_data_pairs:
                if '=' not in p:
                    return {'error': "Could not interpret '%s' in '%s'" % (p, extra_data_str)}

                parts = p.split("=")
                k = parts[0]
                v = "=".join(parts[1:])
                extra_data[k] = v

    result = put_account( args.name, args.service, args.identifier, args.content_url, proxy=proxy, wallet_keys=wallet_keys, required_drivers=required_drivers, **extra_data )
    if 'error' not in result:
        analytics_event( "Put account", {} )

    return result


def cli_advanced_delete_account( args, proxy=None, config_path=CONFIG_PATH, password=None ):
    """
    command: delete_account norpc
    help: Delete a particular account.
    arg: name (str) "The name to query."
    arg: service (str) "The service the account is for."
    arg: identifier (str) "The identifier of the account to delete."
    """

    result = {}
    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir, password=password)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir, password=password)
    if 'error' in res:
        return res

    if not is_name_valid(args.name) or len(args.service) == 0 or len(args.identifier) == 0:
        return {'error': 'Invalid name or identifier'}

    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys
    
    if proxy is None:
        proxy = get_default_proxy(config_path=config_path)

    result = delete_account( args.name, args.service, args.identifier, proxy=proxy, wallet_keys=wallet_keys )
    if 'error' not in result:
        analytics_event( "Delete account", {} )

    return result


def cli_advanced_wallet( args, config_path=CONFIG_PATH, password=None ):
    """
    command: wallet norpc
    help: Query wallet information
    """
    
    result = {}
    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir, password=password)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir, password=password)
    if 'error' in res:
        return res

    wallet_path = os.path.join(config_dir, WALLET_FILENAME)
    if not os.path.exists(wallet_path):
        result = initialize_wallet(wallet_path=wallet_path)

    else:
        result = get_wallet_with_backoff( config_path )
        
        payment_privkey = result.get("payment_privkey", None)
        owner_privkey = result.get("owner_privkey", None)
        data_privkey = result.get("data_privkey", None)

        display_wallet_info(result.get('payment_address'), result.get('owner_address'), result.get('data_pubkey'), config_path=CONFIG_PATH )

        print "-" * 60
        print "Payment private key info: %s" % privkey_to_string( payment_privkey )
        print "Owner private key info:   %s" % privkey_to_string( owner_privkey )
        print "Data private key info:    %s" % privkey_to_string( data_privkey )
        
    return result


def cli_advanced_consensus( args, config_path=CONFIG_PATH ):
    """
    command: consensus
    help: Get current consensus information 
    opt: block_height (int) "The block height at which to query the consensus information.  If not given, the current height is used."
    """
    result = {}
    if args.block_height is None:
        # by default get last indexed block
        resp = getinfo()

        if 'error' in resp:
            return resp

        if 'last_block_processed' in resp and 'consensus_hash' in resp:
            return {'consensus': resp['consensns_hash'], 'block_height': resp['last_block_processed']}

        else:
            return {'error': 'Server is indexing.  Try again shortly.'}

    resp = get_consensus_at(int(args.block_height))

    data = {}
    data['consensus'] = resp
    data['block_height'] = args.block_height

    result = data
    return result


def cli_advanced_rpcctl( args, config_path=CONFIG_PATH ):
    """
    command: rpcctl norpc
    help: Control the background blockstack API endpoint
    arg: command (str) "'start', 'stop', 'restart', or 'status'"
    """

    config_dir = config.CONFIG_DIR
    if config_path is not None:
        config_dir = os.path.dirname(config_path)

    rc = local_rpc.local_rpc_action( str(args.command), config_dir=config_dir )
    if rc != 0:
        return {'error': 'RPC controller exit code %s' % rc}
    else:
        return {'status': True}


def cli_advanced_rpc( args, config_path=CONFIG_PATH ):
    """
    command: rpc norpc
    help: Issue an RPC request to a locally-running API endpoint
    arg: method (str) "The method to call"
    opt: args (str) "A JSON list of positional arguments."
    opt: kwargs (str) "A JSON object of keyword arguments."
    """
    
    rpc_args = []
    rpc_kw = {}

    if args.args is not None:
        try:
            rpc_args = json.loads(args.args)
        except:
            print >> sys.stderr, "Not JSON: '%s'" % args.args
            return {'error': 'Invalid arguments'}

    if args.kwargs is not None:
        try:
            rpc_kw = json.loads(args.kwargs)
        except:
            print >> sys.stderr, "Not JSON: '%s'" % args.kwargs
            return {'error': 'Invalid arguments'}

    conf = config.get_config( path=config_path )
    portnum = conf['api_endpoint_port']
    rpc_kw['config_dir'] = os.path.dirname(config_path)

    result = local_rpc.local_rpc_dispatch( portnum, str(args.method), *rpc_args, **rpc_kw ) 
    return result


def cli_advanced_name_import( args, config_path=CONFIG_PATH ):
    """
    command: name_import norpc
    help: Import a name to a revealed but not-yet-readied namespace
    arg: name (str) "The name to import"
    arg: address (str) "The address of the name recipient"
    arg: hash (str) "The zonefile hash of the name"
    arg: privatekey (str) "One of the private keys of the namespace revealer"
    """
    # BROKEN
    result = name_import(str(args.name), str(args.address),
                         str(args.hash), str(args.privatekey))

    return result


def cli_advanced_namespace_preorder( args, config_path=CONFIG_PATH ):
    """
    command: namespace_preorder norpc
    help: Preorder a namespace
    arg: namespace_id (str) "The namespace ID"
    arg: privatekey (str) "The private key to send and pay for the preorder"
    opt: reveal_addr (str) "The address of the keypair that will import names (automatically generated if not given)"
    """
    # BROKEN
    reveal_addr = None
    if args.address is not None:
        reveal_addr = str(args.address)

    result = namespace_preorder(str(args.namespace_id),
                                str(args.privatekey),
                                reveal_addr=reveal_addr)

    return result


def cli_advanced_namespace_reveal( args, config_path=CONFIG_PATH ):
    """
    command: namespace_reveal norpc
    help: Reveal a namespace and set its pricing parameters
    arg: namespace_id (str) "The namespace ID"
    arg: addr (str) "The address of the keypair that will import names (given in the namespace preorder)"
    arg: lifetime (int) "The lifetime (in blocks) for each name.  Negative means 'never expires'."
    arg: coeff (int) "The multiplicative coefficient in the price function."
    arg: base (int) "The exponential base in the price function."
    arg: bucket_exponents (str) "A 16-field CSV of name-length exponents in the price function."
    arg: nonalpha_discount (int) "The denominator that defines the discount for names with non-alpha characters."
    arg: no_vowel_discount (int) "The denominator that defines the discount for names without vowels."
    arg: privatekey (str) "The private key of the import keypair (whose address is `addr` above)."
    """
    # BROKEN
    bucket_exponents = args.bucket_exponents.split(',')
    if len(bucket_exponents) != 16:
        return {'error': '`bucket_exponents` must be a 16-value CSV of integers'}

    for i in xrange(0, len(bucket_exponents)):
        try:
            bucket_exponents[i] = int(bucket_exponents[i])
        except:
            return {'error': '`bucket_exponents` must contain integers between 0 and 15, inclusively.'}

    lifetime = int(args.lifetime)
    if lifetime < 0:
        lifetime = 0xffffffff       # means "infinite" to blockstack-server

    result = namespace_reveal(str(args.namespace_id),
                              str(args.addr),
                              lifetime,
                              int(args.coeff),
                              int(args.base),
                              bucket_exponents,
                              int(args.nonalpha_discount),
                              int(args.no_vowel_discount),
                              str(args.privatekey))

    return result


def cli_advanced_namespace_ready( args, config_path=CONFIG_PATH ):
    """
    command: namespace_ready norpc
    help: Mark a namespace as ready
    arg: namespace_id (str) "The namespace ID"
    arg: privatekey (str) "The private key of the keypair that imports names"
    """
    # BROKEN
    result = namespace_ready(str(args.namespace_id),
                             str(args.privatekey))

    return result


def cli_advanced_put_mutable( args, config_path=CONFIG_PATH, password=None, proxy=None ):
    """
    command: put_mutable norpc
    help: Put mutable data into a profile
    arg: name (str) "The name to receive the data"
    arg: data_id (str) "The name of the data"
    arg: data (str) "The JSON-formatted data to store"
    """
    fqu = str(args.name)
    error = check_valid_name(fqu)
    if error:
        return {'error': error}

    try:
        data = json.loads(args.data)
    except:
        return {'error': "Invalid JSON"}

    config_dir = os.path.dirname(config_path)
    res = start_rpc_endpoint(config_dir)
    if 'error' in res:
        return res
 
    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    if proxy is None:
        proxy = get_default_proxy()

    result = put_mutable(fqu, str(args.data_id), data, wallet_keys=wallet_keys, proxy=proxy )

    return result


def cli_advanced_put_immutable( args, config_path=CONFIG_PATH, password=None, proxy=None ):
    """
    command: put_immutable norpc
    help: Put immutable data into a zonefile
    arg: name (str) "The name to receive the data"
    arg: data_id (str) "The name of the data"
    arg: data (str) "The JSON-formatted data to store"
    """

    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir, password=password)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir)
    if 'error' in res:
        return res

    fqu = str(args.name)
    error = check_valid_name(fqu)
    if error:
        return {'error': error}

    try:
        data = json.loads(args.data)
    except:
        return {'error': "Invalid JSON"}
 
    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    owner_privkey_info = wallet_keys['owner_privkey']
    payment_privkey_info = wallet_keys['payment_privkey']

    res = operation_sanity_check(fqu, payment_privkey_info, owner_privkey_info, config_path=config_path)
    if 'error' in res:
        return res

    if proxy is None:
        proxy = get_default_proxy()

    result = put_immutable( fqu, str(args.data_id), data, wallet_keys=wallet_keys, proxy=proxy ) 
    return result


def cli_advanced_get_mutable( args, config_path=CONFIG_PATH, proxy=None ):
    """
    command: get_mutable
    help: Get mutable data from a profile
    arg: name (str) "The name that has the data"
    arg: data_id (str) "The name of the data"
    """
    conf = config.get_config( config_path )
    if proxy is None:
        proxy = get_default_proxy()

    result = get_mutable(str(args.name), str(args.data_id), proxy=proxy, conf=conf)
    return result 


def cli_advanced_get_immutable( args, config_path=CONFIG_PATH, proxy=None ):
    """
    command: get_immutable
    help: Get immutable data from a zonefile
    arg: name (str) "The name that has the data"
    arg: data_id_or_hash (str) "Either the name or the SHA256 of the data to obtain"
    """
    if proxy is None:
        proxy = get_default_proxy()

    if is_valid_hash( args.data_id_or_hash ):
        result = get_immutable(str(args.name), str(args.data_id_or_hash), proxy=proxy)
        if 'error' not in result:
            return result

    # either not a valid hash, or no such data with this hash.
    # maybe this hash-like string is the name of something?
    result = get_immutable_by_name(str(args.name), str(args.data_id_or_hash), proxy=proxy)
    return result


def cli_advanced_list_update_history( args, config_path=CONFIG_PATH ):
    """
    command: list_update_history
    help: List the history of update hashes for a name
    arg: name (str) "The name whose data to list"
    """
    result = list_update_history(str(args.name))
    return result


def cli_advanced_list_zonefile_history( args, config_path=CONFIG_PATH ):
    """
    command: list_zonefile_history
    help: List the history of zonefiles for a name (if they can be obtained)
    arg: name (str) "The name whose zonefiles to list"
    """
    result = list_zonefile_history(str(args.name))
    return result


def cli_advanced_list_immutable_data_history( args, config_path=CONFIG_PATH ):
    """
    command: list_immutable_data_history
    help: List all prior hashes of a given immutable datum
    arg: name (str) "The name whose data to list"
    arg: data_id (str) "The data identifier whose history to list"
    """
    result = list_immutable_data_history(str(args.name), str(args.data_id))
    return result


def cli_advanced_delete_immutable( args, config_path=CONFIG_PATH, proxy=None, password=None ):
    """
    command: delete_immutable norpc
    help: Delete an immutable datum from a zonefile.
    arg: name (str) "The name that owns the data"
    arg: hash (str) "The SHA256 of the data to remove"
    """
    
    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir, password=password)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir)
    if 'error' in res:
        return res

    fqu = str(args.name)
    error = check_valid_name(fqu)
    if error:
        return {'error': error}
 
    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    owner_privkey_info = wallet_keys['owner_privkey']
    payment_privkey_info = wallet_keys['payment_privkey']

    res = operation_sanity_check(fqu, payment_privkey_info, owner_privkey_info, config_path=config_path)
    if 'error' in res:
        return res

    if proxy is None:
        proxy = get_default_proxy()

    result = delete_immutable(str(args.name), str(args.hash), proxy=proxy, wallet_keys=wallet_keys )
    return result


def cli_advanced_delete_mutable( args, config_path=CONFIG_PATH ):
    """
    command: delete_mutable norpc
    help: Delete a mutable datum from a profile.
    arg: name (str) "The name that owns the data"
    arg: data_id (str) "The ID of the data to remove"
    """
    result = delete_mutable(str(args.name), str(args.data_id))
    return result


def cli_advanced_get_name_blockchain_record( args, config_path=CONFIG_PATH ):
    """
    command: get_name_blockchain_record
    help: Get the raw blockchain record for a name
    arg: name (str) "The name to list"
    """
    result = get_name_blockchain_record(str(args.name))
    return result


def cli_advanced_get_name_blockchain_history( args, config_path=CONFIG_PATH ):
    """
    command: get_name_blockchain_history
    help: Get a sequence of historic blockchain records for a name
    arg: name (str) "The name to query"
    opt: start_block (int) "The start block height"
    opt: end_block (int) "The end block height"
    """
    start_block = args.start_block
    if start_block is None:
        start_block = FIRST_BLOCK_MAINNET
    else:
        start_block = int(args.start_block)

    end_block = args.end_block
    if end_block is None:
        # I would love to have to update this number in the future,
        # if it proves too small.  That would be a great problem
        # to have :-)
        end_block = 100000000
    else:
        end_block = int(args.end_block)

    result = get_name_blockchain_history( str(args.name), start_block, end_block )
    return result


def cli_advanced_get_namespace_blockchain_record( args, config_path=CONFIG_PATH ):
    """
    command: get_namespace_blockchain_record
    help: Get the raw namespace blockchain record for a name
    arg: namespace_id (str) "The namespace ID to list"
    """
    result = get_namespace_blockchain_record(str(args.namespace_id))
    return result


def cli_advanced_lookup_snv( args, config_path=CONFIG_PATH ):
    """
    command: lookup_snv
    help: Use SNV to look up a name at a particular block height
    arg: name (str) "The name to query"
    arg: block_id (int) "The block height at which to query the name"
    arg: trust_anchor (str) "The trusted consensus hash, transaction ID, or serial number from a higher block height than `block_id`"
    """
    result = lookup_snv(str(args.name), int(args.block_id),
                        str(args.trust_anchor))

    return result


def cli_advanced_get_name_zonefile( args, config_path=CONFIG_PATH ):
    """
    command: get_name_zonefile
    help: Get a name's zonefile
    arg: name (str) "The name to query"
    opt: json (str) "If 'true' is given, try to parse as JSON"
    """
    parse_json = getattr(args, 'json', 'false')
    if parse_json is not None and parse_json.lower() in ['true', '1']:
        parse_json = True
    else:
        parse_json = False

    result = get_name_zonefile(str(args.name), raw_zonefile=True)
    if result is None:
        return {'error': 'Failed to get zonefile'}

    if 'error' in result:
        log.error("get_name_zonefile failed: %s" % result['error'])
        return result
    
    if 'zonefile' not in result:
        return {'error': 'No zonefile data'}

    if parse_json:
        # try to parse
        try:
            new_zonefile = decode_name_zonefile(result['zonefile'] )
            assert new_zonefile is not None
            result['zonefile'] = new_zonefile
        except:
            result['warning'] = 'Non-standard zonefile'

    return result


def cli_advanced_get_names_owned_by_address( args, config_path=CONFIG_PATH ):
    """
    command: get_names_owned_by_address
    help: Get the list of names owned by an address
    arg: address (str) "The address to query"
    """
    result = get_names_owned_by_address(str(args.address))
    return result


def cli_advanced_get_namespace_cost( args, config_path=CONFIG_PATH ):
    """
    command: get_namespace_cost
    help: Get the cost of a namespace
    arg: namespace_id (str) "The namespace ID to query"
    """
    result = get_namespace_cost(str(args.namespace_id))
    return result


def cli_advanced_get_all_names( args, config_path=CONFIG_PATH ):
    """
    command: get_all_names norpc
    help: Get all names in existence, optionally paginating through them
    opt: offset (int) "The offset into the sorted list of names"
    opt: count (int) "The number of names to return"
    """
    offset = None
    count = None

    if args.offset is not None:
        offset = int(args.offset)

    if args.count is not None:
        count = int(args.count)

    result = get_all_names(offset=offset, count=count)
    return result


def cli_advanced_get_names_in_namespace( args, config_path=CONFIG_PATH ):
    """
    command: get_names_in_namespace norpc
    help: Get the names in a given namespace, optionally paginating through them
    arg: namespace_id (str) "The ID of the namespace to query"
    opt: offset (int) "The offset into the sorted list of names"
    opt: count (int) "The number of names to return"
    """
    offset = None
    count = None

    if args.offset is not None:
        offset = int(args.offset)

    if args.count is not None:
        count = int(args.count)

    result = get_names_in_namespace(str(args.namespace_id), offset, count)
    return result


def cli_advanced_get_nameops_at( args, config_path=CONFIG_PATH ):
    """
    command: get_nameops_at
    help: Get the list of name operations that occurred at a given block number
    arg: block_id (int) "The block height to query"
    """
    result = get_nameops_at(int(args.block_id))
    return result


def cli_advanced_set_zonefile_hash( args, config_path=CONFIG_PATH, password=None ):
    """
    command: set_zonefile_hash norpc
    help: Directly set the hash associated with the name in the blockchain.
    arg: name (str) "The name to update"
    arg: zonefile_hash (str) "The RIPEMD160(SHA256(zonefile)) hash"
    """
    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir, password=password)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir, password=password)
    if 'error' in res:
        return res

    fqu = str(args.name)

    error = check_valid_name(fqu)
    if error:
        return {'error': error}

    zonefile_hash = str(args.zonefile_hash)
    if re.match(r"^[a-fA-F0-9]+$", zonefile_hash ) is None or len(zonefile_hash) != 40:
        return {'error': 'Not a valid zonefile hash'}
    
    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    owner_privkey_info = wallet_keys['owner_privkey']
    payment_privkey_info = wallet_keys['payment_privkey']

    res = operation_sanity_check(fqu, payment_privkey_info, owner_privkey_info, config_path=config_path)
    if 'error' in res:
        return res

    rpc = local_rpc_connect(config_dir=config_dir)

    try:
        resp = rpc.backend_update(fqu, None, None, zonefile_hash)
    except Exception, e:
        log.exception(e)
        return {'error': 'Error talking to server, try again.'}

    if 'success' in resp and resp['success']:
        result = resp
    else:
        if 'error' in resp:
            return resp

        if 'message' in resp:
            return {'error': resp['message']}

    analytics_event( "Set zonefile hash", {} )
    return result


def cli_advanced_unqueue( args, config_path=CONFIG_PATH, password=None ):
    """
    command: unqueue norpc
    help: Remove a stuck transaction from the queue.
    arg: name (str) "The affected name"
    arg: queue_id (str) "The type of queue ('preorder', 'register', 'update', etc.)."
    arg: txid (str) "The transaction ID"
    """
    conf = config.get_config(config_path)
    queue_path = conf['queue_path']

    try:
        res = queuedb_remove( str(args.queue_id), str(args.name), str(args.txid), path=queue_path)
    except:
        return {'error': 'Failed to remove from queue\n%s' % traceback.format_exc()}

    return {'status': True}


def cli_advanced_set_profile( args, config_path=CONFIG_PATH, password=None, proxy=None ):
    """
    command: set_profile norpc
    help: Directly set a profile's JSON.
    arg: name (str) "The name to set the profile for"
    arg: data (str) "The profile as a JSON string, or a path to the profile."
    """

    conf = config.get_config(config_path)
    name = str(args.name)
    profile_json_str = str(args.data)

    if proxy is None:
        proxy = get_default_proxy()

    profile = None
    if is_valid_path(profile_json_str) and os.path.exists(profile_json_str):
        # this is a path.  try to load it
        try:
            with open(profile_json_str, "r") as f:
                profile_json_str = f.read()
        except:
            return {'error': 'Failed to load "%s"' % profile_json_str}

    # try to parse it
    try:
        profile = json.loads(profile_json_str)
    except:
        return {'error': 'Invalid profile JSON'}

    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    required_storage_drivers = conf.get('storage_drivers_required_write', config.BLOCKSTACK_REQUIRED_STORAGE_DRIVERS_WRITE)
    required_storage_drivers = required_storage_drivers.split()

    owner_address = get_privkey_info_address(wallet_keys['owner_privkey'])
    user_zonefile = get_name_zonefile( name, proxy=proxy, wallet_keys=wallet_keys )
    if 'error' in user_zonefile:
        return user_zonefile

    user_zonefile = user_zonefile['zonefile']
    if blockstack_profiles.is_profile_in_legacy_format( user_zonefile ):
        return {'error': "Profile in legacy format.  Please migrate it with the 'migrate' command first."}

    res = profile_update( name, user_zonefile, profile, owner_address, proxy=proxy, wallet_keys=wallet_keys, required_drivers=required_storage_drivers )
    if 'error' in res:
        return res
    else:
        return {'status': True}


def cli_advanced_sync_zonefile( args, config_path=CONFIG_PATH, proxy=None, interactive=True, nonstandard=False ):
    """
    command: sync_zonefile
    help: Upload the current zone file to all storage providers.
    arg: name (str) "Name of the zone file to synchronize."
    opt: txid (str) "NAME_UPDATE transaction ID that set the zone file."
    opt: zonefile (str) "The zone file (JSON or text), if unavailable from other sources."
    opt: nonstandard (str) "If true, do not attempt to parse the zonefile.  Just upload as-is."
    """

    conf = config.get_config(config_path)
 
    assert 'server' in conf.keys()
    assert 'port' in conf.keys()
    assert 'queue_path' in conf.keys()

    queue_path = conf['queue_path']
    name = str(args.name)
    if proxy is None:
        proxy = get_default_proxy(config_path)

    txid = None
    if hasattr(args, "txid"):
        txid = getattr(args, "txid")

    if not nonstandard and hasattr(args, "nonstandard"):
        if args.nonstandard.lower() in ['yes', '1', 'true']:
            nonstandard = True

    user_data = None
    zonefile_hash = None

    if hasattr(args, "zonefile") and getattr(args, "zonefile") is not None:
        # zonefile given
        user_data = args.zonefile
        valid = False
        try:
            user_data_res = load_zonefile( name, user_data )
            if 'error' in user_data_res and 'identical' not in user_data_res.keys():
                log.warning("Failed to parse zonefile (reason: %s)" % user_data_res['error'])
            else:
                valid = True
                user_data = user_data_res['zonefile']

        except Exception, e:
            if os.environ.get("BLOCKSTACK_DEBUG", None) == "1":
                log.exception(e)
            valid = False

        # if it's not a valid zonefile, ask if the user wants to sync 
        if not valid and interactive:
            proceed = prompt_invalid_zonefile()
            if not proceed:
                return {'error': 'Not replicating invalid zone file'}
    
        elif not valid and not nonstandard:
            return {'error': 'Not replicating invalid zone file'}

    if txid is None or user_data is None:
    
        # load zonefile and txid from queue?
        queued_data = queuedb_find( "update", name, path=queue_path )
        if len(queued_data) > 0:

            # find the current one (get raw zonefile)
            log.debug("%s updates queued for %s" % (len(queued_data), name))
            for queued_zfdata in queued_data:
                update_data = queue_extract_entry( queued_zfdata )
                zfdata = update_data.get('zonefile', None)
                if zfdata is None:
                    continue

                user_data = zfdata
                txid = queued_zfdata.get('tx_hash', None)
                break

        if user_data is None:
            # not in queue.  Maybe it's available from one of the storage drivers?
            log.debug("no pending updates for '%s'; try storage" % name)
            user_data = get_name_zonefile( name, raw_zonefile=True )
            if user_data is None:
                user_data = {'error': 'No data loaded'}
 
            if 'error' in user_data:
                log.error("Failed to get zonefile: %s" % user_data['error'])
                return user_data

            user_data = user_data['zonefile']

        # have user data
        zonefile_hash = storage.get_zonefile_data_hash( user_data )

        if txid is None:
            # not in queue.  Fetch from blockstack server
            name_rec = get_name_blockchain_record( name )
            if 'error' in name_rec:
                log.error("Failed to get name record for %s: %s" % (name, name_rec['error']))
                return {'error': "Failed to get name record to look up tx hash."}

            # find the tx hash that corresponds to this zonefile
            if name_rec['op'] == NAME_UPDATE:
                if name_rec['value_hash'] == zonefile_hash:
                    txid = name_rec['txid']
                
            else:
                name_history = name_rec['history']
                for history_key in reversed(sorted(name_rec['history'])):
                    if name_history[history_key].has_key('op') and name_history[history_key]['op'] == NAME_UPDATE:
                        if name_history[history_key].has_key('value_hash') and name_history[history_key]['value_hash'] == zonefile_hash:
                            if name_history[history_key].has_key('txid'):
                                txid = name_history[history_key]['txid']
                                break
        
        if txid is None:
            log.error("Unable to lookup txid for update %s, %s" % (name, zonefile_hash))
            return {'error': "Unable to lookup txid that wrote zonefile"}
 
    # can proceed to replicate
    res = zonefile_data_replicate( name, user_data, txid, [(conf['server'], conf['port'])], config_path=config_path )
    if 'error' in res:
        log.error("Failed to replicate zonefile: %s" % res['error'])
        return res
 
    return {'status': True, 'value_hash': zonefile_hash}


def cli_advanced_convert_legacy_profile( args, config_path=CONFIG_PATH ):
    """
    command: convert_legacy_profile norpc
    help: Convert a legacy profile into a modern profile.
    arg: path (str) "Path on disk to the JSON file that contains the legacy profile data from Onename"
    """

    profile_json_str = None
    profile = None

    try:
        with open(args.path, "r") as f:
            profile_json_str = f.read()

        profile = json.loads(profile_json_str)
    except:
        return {'error': 'Failed to load profile JSON'}

    # should have 'profile' key
    if not profile.has_key('profile'):
        return {'error': 'JSON has no "profile" key'}

    profile = profile['profile']
    profile = blockstack_profiles.get_person_from_legacy_format( profile )
    return profile


def cli_advanced_app_register( args, config_path=CONFIG_PATH, password=None, proxy=None, interactive=True ):
    """
    command: app_register norpc
    help: Register a new application with your profile.
    arg: name (str) "The name to link the app to"
    arg: app_name (str) "The name of the application"
    arg: app_account_id (str) "The name of the application account"
    arg: app_url (str) "The URL to the application"
    opt: storage_drivers (str) "A CSV of storage drivers to host this app's data"
    opt: app_password (str) "The application-specific wallet password"
    opt: app_fields (str) "A CSV of application-specific key/value pairs"
    """

    if proxy is None:
        proxy = get_default_proxy(config_path=config_path)

    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir, password=password)
    if 'error' in res:
        return res

    fqu = str(args.name)
    error = check_valid_name(fqu)
    if error:
        return {'error': error}

    app_name = str(args.app_name)
    app_account_id = str(args.app_account_id)
    app_url = str(args.app_url)
    app_storage_drivers = args.app_storage_drivers
    app_fields = args.app_fields
    app_password = args.app_password

    if len(app_name) == 0:
        return {'error': 'Invalid app name'}

    if len(app_account_id) == 0:
        return {'error': 'Invalid app account ID'}

    if len(app_url) == 0:
        return {'error': 'Invalid app URL'}

    if app_password is None:
        interactive = True

    if app_storage_drivers:
        app_storage_drivers = str(app_storage_drivers)
        app_storage_drivers = app_storage_drivers.split(",")
    else:
        app_storage_drivers = None

    if app_fields:
        app_fields = str(app_fields)
        try:
            tmp = ",".split(app_fields)
            app_fields = {}
            for kv in tmp:
                p = kv.strip().split("=")
                assert len(p) > 1, "Invalid key/value list"
                k = p[0]
                v = "=".join(p[1:])
                app_fields[k] = v
        except AssertionError:
            return {'error': "Invalid key/value list"}
        except Exception, e:
            log.exception(e)
            return {'error': 'Invalid key/value list'}

    else:
        app_fields = {}

    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys
    
    res = app_register( fqu, app_name, app_account_id, app_url, app_storage_drivers=app_storage_drivers, app_account_fields=app_fields, wallet_keys=wallet_keys, password=app_password, interactive=interactive, config_path=config_path )
    return res


def cli_advanced_app_unregister( args, config_path=CONFIG_PATH, password=None, interactive=True ):
    """
    command: app_unregister norpc
    help: Unregister an application from a profile
    arg: name (str) "The name that owns the app account"
    arg: app_name (str) "The name of the application"
    arg: app_account_id (str) "The name of the application account"
    """

    name = args.name
    app_name = args.app_name
    app_account_id = args.app_account_id

    if proxy is None:
        proxy = get_default_proxy(config_path=config_path)

    config_dir = os.path.dirname(config_path)
    res = wallet_ensure_exists(config_dir)
    if 'error' in res:
        return res

    res = start_rpc_endpoint(config_dir, password=password)
    if 'error' in res:
        return res

    fqu = str(args.name)
    error = check_valid_name(fqu)
    if error:
        return {'error': error}

    app_name = str(args.app_name)
    app_account_id = str(args.app_account_id)

    if len(app_name) == 0:
        return {'error': 'Invalid app name'}

    if len(app_account_id) == 0:
        return {'error': 'Invalid app account ID'}

    wallet_keys = get_wallet_keys( config_path, password )
    if 'error' in wallet_keys:
        return wallet_keys

    res = app_unregister( fqu, app_name, app_account_id, interactive=interactive, wallet_keys=wallet_keys, proxy=proxy, config_path=config_path )
    return res


def cli_advanced_app_get_wallet( args, config_path=CONFIG_PATH, interactive=True ):
    """
    command: app_get_wallet
    help: Get an application account wallet
    arg: name (str) "The name that owns the app account"
    arg: app_name (str) "The name of the application"
    arg: app_account_id (str) "The name of the application account"
    opt: app_password (str) "The app wallet password"
    """

    fqu = str(args.name)
    error = check_valid_name(fqu)
    if error:
        return {'error': error}

    app_name = str(args.app_name)
    app_account_id = str(args.app_account_id)
    password = args.app_password

    if len(app_name) == 0:
        return {'error': 'Invalid app name'}

    if len(app_account_id) == 0:
        return {'error': 'Invalid app account ID'}

    if password:
        password = str(password)
    else:
        password = None
        interactive = True
    
    res = app_get_wallet( fqu, app_name, app_account_id, interactive=interactive, password=password, config_path=config_path )
    return res


def cli_advanced_start_server( args, config_path=CONFIG_PATH, interactive=False ):
    """
    command: start_server norpc
    help: Start a Blockstack server
    opt: foreground (str) "If True, then run in the foreground."
    opt: working_dir (str) "The directory which contains the server state."
    opt: testnet (str) "If True, then communicate with Bitcoin testnet."
    """

    foreground = False
    testnet = False
    working_dir = args.working_dir

    if args.foreground:
        foreground = str(args.foreground)
        foreground = (foreground.lower() in ['1', 'true', 'yes', 'foreground'])

    if args.testnet:
        testnet = str(args.testnet)
        testnet = (testnet.lower() in ['1', 'true', 'yes', 'testnet'])

    cmds = ['blockstack-server', 'start']
    if foreground:
        cmds.append('--foreground')

    if testnet:
        cmds.append('--testnet')

    if working_dir is not None:
        working_dir_envar = 'VIRTUALCHAIN_WORKING_DIR={}'.format(working_dir)
        cmds = [working_dir_envar] + cmds

    cmd_str = " ".join(cmds)
    
    log.debug('Execute: {}'.format(cmd_str))
    exit_status = os.system(cmd_str)

    if not os.WIFEXITED(exit_status) or os.WEXITSTATUS(exit_status) != 0:
        error_str = 'Failed to execute "{}". Exit code {}'.format(cmd_str, exit_status)
        return {'error': error_str}

    return {'status': True}


def cli_advanced_stop_server( args, config_path=CONFIG_PATH, interactive=False ):
    """
    command: stop_server norpc
    help: Stop a running Blockstack server
    opt: working_dir (str) "The directory which contains the server state."
    """

    working_dir = args.working_dir

    cmds = ['blockstack-server', 'stop']

    if working_dir is not None:
        working_dir_envar = 'VIRTUALCHAIN_WORKING_DIR={}'.format(working_dir)
        cmds = [working_dir_envar] + cmds

    cmd_str = " ".join(cmds)

    log.debug('Execute: {}'.format(cmd_str))
    exit_status = os.system(cmd_str)

    if not os.WIFEXITED(exit_status) or os.WEXITSTATUS(exit_status) != 0:
        error_str = 'Failed to execute "{}". Exit code {}'.format(cmd_str, exit_status)
        return {'error': error_str}

    return {'status': True}

