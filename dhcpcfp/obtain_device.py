# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
# Copyright 2016 juga <juga@riseup.net>
# This file is part of dhcpcfp.
"""."""
import logging
import sqlite3

logger = logging.getLogger('dhcpcfp')

QUERY_BASE = """select distinct
device.name,
comb_dhcp_mac.version
from comb_dhcp_mac, dhcp_fingerprint, dhcp_vendor, device
where comb_dhcp_mac.dhcp_fingerprint_id=dhcp_fingerprint.id and
comb_dhcp_mac.dhcp_vendor_id=dhcp_vendor.id and
comb_dhcp_mac.device_id=device.id"""
QUERY_END = " order by comb_dhcp_mac.score desc;"
QUERY_FP = """ and dhcp_fingerprint.value=?"""
QUERY_VENDOR = """ and dhcp_vendor.value=?"""

QUERY_BASE_MAC = """select distinct
device.name,
comb_dhcp_mac.version, mac_vendor.name
from comb_dhcp_mac, dhcp_fingerprint, dhcp_vendor, device, mac_vendor
where comb_dhcp_mac.dhcp_fingerprint_id=dhcp_fingerprint.id and
comb_dhcp_mac.dhcp_vendor_id=dhcp_vendor.id and
comb_dhcp_mac.device_id=device.id and
comb_dhcp_mac.mac_vendor_id=mac_vendor.id and
(dhcp_fingerprint_id!=0 or dhcp_vendor_id!=0)"""
QUERY_MAC = """ and mac_vendor.mac=?"""


def create_query(dhcp_fingerprint=None, dhcp_vendor=None):
    query = QUERY_BASE
    if dhcp_fingerprint is not None and dhcp_vendor is not None:
        query += QUERY_FP + QUERY_VENDOR + QUERY_END
        params = (dhcp_fingerprint, dhcp_vendor)
    elif dhcp_fingerprint is not None:
        query += QUERY_FP + QUERY_END
        params = (dhcp_fingerprint,)
    elif dhcp_vendor is not None:
        query += QUERY_VENDOR + QUERY_END
        params = (dhcp_vendor,)
    logger.debug(query)
    logger.debug(params)
    return (query, params)


def create_query_mac(mac_vendor, dhcp_fingerprint=None, dhcp_vendor=None):
    query = QUERY_BASE_MAC
    if dhcp_fingerprint is not None and dhcp_vendor is not None:
        query += QUERY_FP + QUERY_VENDOR + QUERY_MAC + QUERY_END
        params = (dhcp_fingerprint, dhcp_vendor, mac_vendor)
    elif dhcp_fingerprint is not None:
        query += QUERY_FP + QUERY_MAC + QUERY_END
        params = (dhcp_fingerprint, mac_vendor)
    elif dhcp_vendor is not None:
        query += QUERY_VENDOR + QUERY_MAC + QUERY_END
        params = (dhcp_vendor, mac_vendor)
    logger.debug(query)
    logger.debug(params)
    return (query, params)


def query_db(db, query, params):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    rows = c.execute(query, params)
    return rows


def gen_device_text(rows):
    text = '. '.join([', '.join([i or u'' for i in row]) for row in rows])
    return text


def device_from_fp(db, dhcp_fingerprint=None, dhcp_vendor=None):
    query, params = create_query(dhcp_fingerprint, dhcp_vendor)
    rows = query_db(db, query, params)
    text = gen_device_text(rows)
    return text


def device_from_fp_mac(db, mac_vendor, dhcp_fingerprint=None,
                       dhcp_vendor=None):
    query, params = create_query_mac(mac_vendor, dhcp_fingerprint, dhcp_vendor)
    rows = query_db(db, query, params)
    text = gen_device_text(rows)
    return text
