# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
# Copyright 2016 juga <juga@riseup.net>
# This file is part of dhcpcfp.
"""."""
import logging
import sqlite3

from .conflog import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('dhcpcfp')

QUERY_BASE = """select distinct
device.mobile, device.tablet, device.name,
comb_dhcp_distinct.version
from comb_dhcp_distinct, dhcp_fingerprint, dhcp_vendor, device
where comb_dhcp_distinct.dhcp_fingerprint_id=dhcp_fingerprint.id and
comb_dhcp_distinct.dhcp_vendor_id=dhcp_vendor.id and
comb_dhcp_distinct.device_id=device.id"""
QUERY_END = " order by comb_dhcp_distinct.score desc;"
QUERY_FP = """ and dhcp_fingerprint.value=?"""
QUERY_VENDOR = """ and dhcp_vendor.value=?"""


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
        params = (dhcp_vendor)
    logger.debug(query)
    logger.debug(params)
    return (query, params)


def query_db(db, query, params):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    rows = c.execute(query, params)
    return rows


def gen_device_text(rows):
    lines = []
    for row in rows:
        row = list(row)
        if row[2] is None:
            row[2] = u''
        if row[3] is None:
            row[3] = u''
        if row[0] is 1:
            row[0] = 'mobile'
        elif row[1] is 1:
            row[0] = 'tablet'
        else:
            row[0] = 'computer'
        row.pop(1)
        lines.append(', '.join(row))
    text = '\n'.join(lines)
    return text


def device_from_fp(db, dhcp_fingerprint=None, dhcp_vendor=None):
    query, params = create_query(dhcp_fingerprint, dhcp_vendor)
    rows = query_db(db, query, params)
    text = gen_device_text(rows)
    return text
