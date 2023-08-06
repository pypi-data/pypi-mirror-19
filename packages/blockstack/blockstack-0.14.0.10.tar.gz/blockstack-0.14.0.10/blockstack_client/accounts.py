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

import argparse
import sys
import json
import traceback
import types
import socket
import uuid
import os
import importlib
import pprint
import random
import time
import copy
import blockstack_profiles
import urllib

import pybitcoin
import bitcoin
import binascii
from utilitybelt import is_hex

from .keys import *
from .proxy import *
from .profile import *

from config import get_logger, DEBUG, MAX_RPC_LEN, find_missing, BLOCKSTACKD_SERVER, \
    BLOCKSTACKD_PORT, BLOCKSTACK_METADATA_DIR, BLOCKSTACK_DEFAULT_STORAGE_DRIVERS, \
    FIRST_BLOCK_MAINNET, NAME_OPCODES, OPFIELDS, CONFIG_DIR, SPV_HEADERS_PATH, BLOCKCHAIN_ID_MAGIC, \
    NAME_PREORDER, NAME_REGISTRATION, NAME_UPDATE, NAME_TRANSFER, NAMESPACE_PREORDER, NAME_IMPORT, \
    USER_ZONEFILE_TTL, CONFIG_PATH

log = get_logger()

import virtualchain


def get_profile_accounts( profile, service_id, account_id ):
    """
    List all accounts in a profile with the given service ID and account ID.
    """
    accounts = profile.get('account', [])
    
    ret = []
    for acc in accounts:
        if acc.get('identifier', None) == account_id and acc.get('service', None) == service_id:
            ret.append(acc)

    return ret


def list_accounts( name, proxy=None ):
    """
    List all of the accounts in a user's profile
    Each account will have at least the following:
        service:  the type of service
        identifier:  a type-specific ID
        role:  a type-specific role

    Return {'error': ...} on error
    """

    if proxy is None:
        proxy = get_default_proxy()

    user_profile, user_zonefile = get_name_profile( name, proxy=proxy )
    if user_profile is None:
        # user_zonefile will contain an error message
        return user_zonefile
        
    # user_profile will be in the new zonefile format 
    if not user_profile.has_key("account"):
        return {'accounts': []}

    else:
        return {'accounts': user_profile['account']}


def get_account( name, service, identifier, proxy=None ):
    """
    Get an account by identifier.  Return duplicates
    Return {'account': account information} on success
    Return {'error': ...} on error
    """
    if proxy is None:
        proxy = get_default_proxy()

    accounts = list_accounts( name, proxy=proxy )
    if 'error' in accounts:
        return accounts

    ret = []
    for acc in accounts['accounts']:
        if acc.get('identifier', None) == identifier and acc.get('service', None) == service:
            ret.append(acc)

    return {'account': ret}


def put_account( name, service, identifier, content_url, create=True, replace=False, proxy=None, wallet_keys=None, txid=None, required_drivers=None, **extra_fields ):
    """
    Put an account's information into a profile.

    If @create is True and @replace is False, then this method appends a new account with @service and @identifier (even if one already exists)
    If @create is True and @replace is True, then this method creates an account and replaces one that has the same @service and @identifier.
        If there are no accounts to replace, then a new account is created.
    If @create is False and @replace is True, then this method replaces an existing account with the same @service and @identifier.
        If there are no such accounts, then this method fails.

    NOTE: the account must already be in the latest form.

    Return a dict with {'status': True} on success (optionally also with 'transaction_hash' set if we updated the zonefile)
    Return a dict with {'error': ...} set on failure.
    """

    if create is False and replace is False:
        return {'error': 'Invalid create/replace arguments'}

    if proxy is None:
        proxy = get_default_proxy()

    need_update = False

    user_profile, user_zonefile, need_update = get_and_migrate_profile( name, proxy=proxy, create_if_absent=True, wallet_keys=wallet_keys, include_name_record=True )
    if 'error' in user_profile:
        return user_profile

    if need_update:
        return {'error': 'Profile is in legacy format.  Please migrate it with the `migrate` command.'}

    name_record = user_zonefile['name_record']
    del user_zonefile['name_record']

    user_zonefile = user_zonefile['zonefile']
    user_profile = user_profile['profile']

    # user_profile will be in the new zonefile format 
    if not user_profile.has_key("account"):
        user_profile['account'] = []

    new_account = {}
    new_account.update( extra_fields )
    new_account.update( {
        "service": service,
        "identifier": identifier,
        "contentUrl": content_url
    })

    replaced = False
    if replace:
        # replace one instance of this account
        for i in xrange(0, len(user_profile['account'])):
            acc = user_profile['account'][i]
            if acc['identifier'] == identifier and acc['service'] == service:
                user_profile['account'][i] = new_account
                replaced = True
                break
            
    if not replaced:
        if create:
            user_profile['account'].append( new_account )
        else:
            return {'error': 'No such existing account'}
        
    return profile_update( name, user_zonefile, user_profile, name_record['address'], proxy=proxy, wallet_keys=wallet_keys, required_drivers=required_drivers )


def delete_account( name, service, identifier, proxy=None, wallet_keys=None ):
    """
    Remove an account's information.
    Return {'status': True, 'removed': [list of removed accounts], ...} on success
    Return {'error': ...} on error
    """

    if proxy is None:
        proxy = get_default_proxy()

    need_update = False 
    removed = False

    user_profile, user_zonefile, need_update = get_and_migrate_profile( name, proxy=proxy, create_if_absent=True, wallet_keys=wallet_keys, include_name_record=True )
    if 'error' in user_profile:
        return user_profile 

    if need_update:
        return {'error': 'Profile is in legacy format.  Please migrate it with the `migrate` command.'}

    name_record = user_zonefile['name_record']
    del user_zonefile['name_record']
    
    user_zonefile = user_zonefile['zonefile']
    user_profile = user_profile['profile']

    # user_profile will be in the new zonefile format
    removed = []
    for account in user_profile.get('account', []):
        if account['service'] == service and account['identifier'] == identifier:
            user_profile['account'].remove( account )
            removed.append( account )

    if len(removed) == 0:
        return {'status': True, 'removed': []}

    else:
        res = profile_update( name, user_zonefile, user_profile, name_record['address'], proxy=proxy, wallet_keys=wallet_keys )
        if 'error' in res:
            return res 

        else:
            res['removed'] = removed
            return res


def create_app_account( name, service, identifier, app_url, storage_drivers, data_pubkey, proxy=None, wallet_keys=None, **extra_fields):
    """
    Make a Blockstck application account.
    This account is different than one created by `put_account`, since
    it is constructed specifically for Blockstack applications.
    It has a few other goodies in it.

    Return {'status': True} on success
    Return {'error': ...} on failure

    Raise on invalid input
    """

    if storage_drivers is None or len(storage_drivers) == 0:
        raise ValueError("No storage drivers given")

    return put_account( name, service, identifier, app_url, create=True, replace=False,
                        proxy=proxy, wallet_keys=wallet_keys,
                        data_pubkey=data_pubkey, storage_drivers=storage_drivers, **extra_fields)


def delete_app_account( name, service, identifier, wallet_keys=None, proxy=None ):
    """
    Delete an application-specific account

    Return {'status': True} on success
    Return {'error': ...} on failure
    """

    res = delete_account( name, service, identifier, proxy=proxy, wallet_keys=wallet_keys )
    if 'error' in res:
        return res

    else:
        return {'status': True}

