# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
# Copyright 2016 juga <juga@riseup.net>
# This file is part of dhcpcfp.
"""."""
import argparse
import logging
import logging.config
import sys

from scapy.all import *

from .conflog import LOGGING
from .constants import BOOTPAP_OPTS, DHCPAP_OPTS, PRL_OPTS

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('dhcpcfp')


def sniff_request(mac, ismymac=False, allpkts=False):
    logger.debug('sniffing')
    if ismymac is True and allpkts is True:
        sniff_filter = "udp and src port 68 and dst port 67"
        # and ether[284] = 3
    else:
        sniff_filter = "udp and src port 68 and dst port 67" \
                       " and ether src {}".format(mac)
                       # and ether[284] = 3

    ans = sniff(iface=conf.iface, count=1,
                filter=sniff_filter,
                lfilter=lambda (p): DHCP in p and
                                    p[DHCP].options[0][1] == 3)
    p = ans[0]
    logger.debug('got a request packet')
    return p


def process_request(r):
    logger.debug('processing request')
    logger.debug('BOOTP fields: %s', r[BOOTP].fields.keys())
    bootp_diff = set(r[BOOTP].fields.keys()).difference(BOOTPAP_OPTS)
    logger.info('BOOTP options not in the Anonymity Profile: %s',
                [(k, r[BOOTP].fields[k]) for k in bootp_diff])
    dhcp_opt_dict = dict([opt for opt in r[DHCP].options
                          if isinstance(opt, tuple) and len(opt) == 2])
    logger.debug('DHCP options: %s', dhcp_opt_dict.keys())
    dhcp_diff = set(dhcp_opt_dict.keys()).difference(DHCPAP_OPTS)
    logger.info('DHCP options not in the Anonymity Profile: %s',
                [(k, dhcp_opt_dict[k]) for k in dhcp_diff])
    dhcp_prl = [ord(o) for o in dhcp_opt_dict['param_req_list']]
    dhcp_prl_names = ', '.join([PRL_OPTS.get(o) for o in dhcp_prl])
    dhcp_fp = ','.join([str(o) for o in dhcp_prl])
    logger.info('PRL options %s', dhcp_prl_names)

    dhcp_vendor = dhcp_opt_dict.get('vendor_class_id')
    data = {
            'bootp_diff': bootp_diff,
            'dhcp_diff': dhcp_diff,
            'dhcp_prl_names': dhcp_prl_names,
            'dhcp_fp': dhcp_fp,
            'dhcp_vendor': dhcp_vendor,
        }
    return data


def check_iface(iface):
    if iface not in get_if_list():
        logger.error('The interface could not be found.')
        sys.exit(1)
    conf.iface = iface


def check_is_my_mac(mac):
    mymac = get_if_hwaddr(conf.iface)
    if mac is not None and mac != mymac:
        logger.warning('Listening for traffic to a MAC that is not'
                       ' any of your own, implies -a, use at your own risk.')
        conf.checkIPaddr = False
        return (mac, False)
    return (mymac, True)
