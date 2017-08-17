# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
# Copyright 2016 juga <juga@riseup.net>
# This file is part of dhcpcfp.
"""."""
import logging
import sys

from scapy.arch import get_if_hwaddr
from scapy.arch.linux import get_if_list
from scapy.config import conf
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sniff
from scapy.utils import str2mac

from .constants import (BOOTPAP_OPTS, DHCPAP_OPTS, FILTER_DHCP,
                        FILTER_DHCP_MAC, PRL_OPTS)
from .obtain_device import device_from_fp, device_from_fp_mac
from .report import write_md_report
from .template import content
from .template_simple import content_simple

logger = logging.getLogger('dhcpcfp')


def is_request(p):
    return DHCP in p and p[DHCP].options[0][1] == 3


def sniff_dhcp(db, outpath, mac, ismymac=False, allpkts=False,
               continuous=False):
    logger.debug('sniffing')
    if ismymac is True and allpkts is True:
        sniff_filter = FILTER_DHCP
    else:
        sniff_filter = FILTER_DHCP_MAC.format(mac)
    if not continuous:
        ans = sniff(iface=conf.iface,
                    filter=sniff_filter,
                    lfilter=lambda p: is_request(p))
        logger.debug('Got a DHCP request packet.')
        show_info_detailed(ans[0], db, outpath)
    sniff(iface=conf.iface,
          filter=sniff_filter,
          lfilter=lambda p: is_request(p),
          prn=lambda x: show_info(x, db, outpath))


def sniff_pcap(pcapfile, db, outpath):
    # pkts = rdpcap(pcapfile)
    sniff(sniff_filter=FILTER_DHCP,
          lfilter=lambda p: is_request(p),
          prn=lambda x: show_info(x, db, outpath),
          offline=pcapfile)


def show_info_detailed(r, db, outpath):
    logger.debug('Processing request')
    logger.debug('BOOTP fields: %s', r[BOOTP].fields.keys())
    bootp_diff = set(r[BOOTP].fields.keys()).difference(BOOTPAP_OPTS)
    logger.info('BOOTP options not in the Anonymity Profile: %s',
                [(k, r[BOOTP].fields[k]) for k in bootp_diff])
    mac = r[Ether].src
    mac_vendor = ''.join(mac.split(':')[:3])
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

    client_id = dhcp_opt_dict.get('client_id')
    if client_id is not None and len(client_id) == 7:
        m = str2mac(client_id[1:])
        if m != mac:
            logger.info('Using client identifier that is not MAC address.')
    else:
        logger.info('Using client identifier that is not MAC address.')

    devices = device_from_fp(db, dhcp_fp, dhcp_vendor)
    logger.info('Guessed devices: %s', devices[:100])
    devices_mac = device_from_fp_mac(db, mac_vendor, dhcp_fp, dhcp_vendor)
    logger.info('Guessed devices using MAC: %s', devices_mac[:100])
    data = {
            'bootp_diff': bootp_diff,
            'dhcp_diff': dhcp_diff,
            'dhcp_prl_names': dhcp_prl_names,
            'dhcp_fp': dhcp_fp,
            'dhcp_vendor': dhcp_vendor,
            'mac_vendor': mac_vendor,
            'devices': devices,
            'devices_mac': devices_mac
        }
    write_md_report(data, content, outpath, False)


def show_info(r, db, outpath):
    logger.debug('Processing request in continuous mode.')
    mac = r[Ether].src
    mac_vendor = ''.join(mac.split(':')[:3])
    dhcp_opt_dict = dict([opt for opt in r[DHCP].options
                          if isinstance(opt, tuple) and len(opt) == 2])
    dhcp_prl = [ord(o) for o in dhcp_opt_dict['param_req_list']]
    dhcp_fp = ','.join([str(o) for o in dhcp_prl])
    logger.info('DHCP Parameter Request List options: %s', dhcp_fp)
    dhcp_vendor = dhcp_opt_dict.get('vendor_class_id')
    logger.info('DHCP vendor: %s', dhcp_vendor)

    client_id = dhcp_opt_dict.get('client_id')
    if client_id is not None and len(client_id) == 7:
        m = str2mac(client_id[1:])
        if m != mac:
            logger.info('Using client identifier that is not MAC address.')
    else:
        logger.info('Using client identifier that is not MAC address.')

    devices = device_from_fp(db, dhcp_fp, dhcp_vendor)
    logger.info('Guessed devices: %s', devices[:100])
    devices_mac = device_from_fp_mac(db, mac_vendor, dhcp_fp, dhcp_vendor)
    logger.info('Guessed devices using MAC: %s', devices_mac[:100])
    data = {
        'dhcp_fp': dhcp_fp,
        'dhcp_vendor': dhcp_vendor,
        'mac_vendor': mac_vendor,
        'devices': devices,
        'devices_mac': devices_mac
        }

    write_md_report(data, content_simple, outpath, True)


def check_iface(iface):
    if iface not in get_if_list():
        logger.error('The interface could not be found.')
        sys.exit(1)
    conf.iface = iface


def check_is_my_mac(mac):
    mymac = get_if_hwaddr(conf.iface)
    if mac is not None and mac != mymac:
        logger.warning('Listening for traffic of a MAC that is not'
                       ' your own, implies -a, use at your own risk!!')
        conf.checkIPaddr = False
        return (mac, False)
    return (mymac, True)
