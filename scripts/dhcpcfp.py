#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
# Copyright 2016 juga <juga@riseup.net>
# This file is part of dhcpcfp.
"""."""
import sys
import os.path
import argparse
import logging
import logging.config
from scapy.config import conf


directory, basename = os.path.split(sys.argv[0])
path, directory = os.path.split(os.path.realpath(directory))
if directory == 'scripts':
    module_path = os.path.realpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        '..'
                    )
                )
    sys.path.insert(0, module_path)

from dhcpcfp.conflog import LOGGING
from dhcpcfp.dhcpcfp import sniff_request, process_request
from dhcpcfp.dhcpcfp import write_md_report, check_iface
from dhcpcfp.dhcpcfp import check_is_my_mac
from dhcpcfp.report_template import content
from dhcpcfp import __version__


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('dhcpcfp')
logger_scapy_interactive = logging.getLogger('scapy.interactive')

TEMPLATE_PATH = os.path.join(module_path, 'templates', 'report.html')
# TEMPLATE_MD_PATH = os.path.join(module_path, 'report_template.py')
OUTPUT_PATH = os.path.join(path, 'output.html')
OUTPUT_MD_PATH = os.path.join(path, 'output.md')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('interface', nargs='?',
                        help='Interface where to listen for DHCP.')
    parser.add_argument('-v', '--verbose',
                        help='Set logging level to debug',
                        action='store_true')
    parser.add_argument('--version', action='version',
                        help='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('mac', nargs='?',
                        help='MAC address to listen for DHCP traffic.')
    parser.add_argument('-a', '--all',
                        help='Not recommended, use at your own risk.',
                        action='store_true')
    parser.add_argument('-o', '--output',
                        help='Report path.')
    args = parser.parse_args()

    conf.sniff_promisc = conf.promisc = 0
    conf.checkIPaddr = 1

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger_scapy_interactive.setLevel(logging.DEBUG)
    if args.interface:
        conf.iface = args.interface
    logger.debug('interface %s' % conf.iface)

    mac, ismymac = check_is_my_mac(args.mac)
    if args.all:
        conf.checkIPaddr = 0
        conf.sniff_promisc = conf.promisc = 1
        logger.warning('Listening for all traffic'
                       ', use at your own risk.')
    if args.output:
        report_md_path = args.output
    else:
        report_md_path = OUTPUT_MD_PATH
    conf.logLevel = 20
    # TODO: listen only in interface or only on mac or all
    p = sniff_request(mac, ismymac, args.all)
    data = process_request(p)
    # write_html_report(data, TEMPLATE_PATH, reportpath)
    write_md_report(data, content, report_md_path)


if __name__ == '__main__':
    main()
