#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
# Copyright 2016 juga <juga@riseup.net>
# This file is part of dhcpcfp.
"""."""
import argparse
import logging
import logging.config
import os.path

from scapy.config import conf

import colorlog

from . import __version__
from .conflog import LOGGING
from .obtain_device import device_from_fp
from .scan_dhcp import check_iface, check_is_my_mac, sniff_dhcp, sniff_pcap

logging.config.dictConfig(LOGGING)
logger = colorlog.getLogger('dhcpcfp')

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
OUTPUT_MD_PATH = os.path.join(path, 'output.md')
DB = os.path.join(path, 'data', 'dhcpfp.db')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        help='Set logging level to debug',
                        action='store_true')
    parser.add_argument('--version', action='version',
                        help='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('-f', '--fingerprint',
                        help='DHCP fingerprint.')
    parser.add_argument('-e', '--vendor',
                        help='DHCP vendor.')
    parser.add_argument('-i', '--interface',
                        help='Interface where to listen for DHCP.')
    parser.add_argument('-m', '--mac',
                        help='MAC address to listen for DHCP traffic.')
    parser.add_argument('-a', '--all',
                        help='Not recommended, use at your own risk.',
                        action='store_true')
    parser.add_argument('-o', '--output',
                        help='Report path.',
                        default=OUTPUT_MD_PATH)
    parser.add_argument('-d', '--db',
                        help='DB path with DHCP fingerprints.',
                        default=DB)
    parser.add_argument('-p', '--pcapfile',
                        help='Obtain devices from pcap dump instead of '
                             'scanning.')
    parser.add_argument('-c', '--continuous',
                        help='Scan until user cancel.',
                        action='store_true')
    args = parser.parse_args()

    conf.sniff_promisc = conf.promisc = 0
    conf.checkIPaddr = 1

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        # logger_scapy_interactive.setLevel(logging.DEBUG)

    if args.fingerprint or args.vendor:
        devices = device_from_fp(args.db, args.fingerprint, args.vendor)
        print(devices)
        exit()
    if args.pcapfile:
        logger.debug('Processing pcap file.')
        sniff_pcap(args.pcapfile, args.db, args.output)
        exit()
    if args.interface:
        check_iface(args.interface)
        conf.iface = args.interface
    logger.debug('Interface: %s' % conf.iface)
    mac, ismymac = check_is_my_mac(args.mac)
    if args.all:
        conf.checkIPaddr = 0
        conf.sniff_promisc = conf.promisc = 1
        logger.warning('Listening for all traffic'
                       ', use at your own risk.')
    # TODO: listen only in interface or only on mac or all
    sniff_dhcp(args.db, args.output, mac, ismymac, args.all,
               args.continuous)


if __name__ == '__main__':
    main()
