# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab

# Copyright 2016 juga <juga@riseup.net>

# This file is part of dhcpcfp.
#
# dhcpcfp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dhcpcfp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dhcpcfp.  If not, see <http://www.gnu.org/licenses/>.

import os
import logging
from dhcpcfp.report import write_md_report
from dhcpcfp.template import content

logger = logging.getLogger('dhcpcfp')

data = {
    'bootp_diff': set(),
    'dhcp_diff': set(['param_req_list']),
    'dhcp_prl_names':
        ['Subnet Mask', 'Broadcast Address', 'Time Offset', 'Router',
         'Domain Name', 'Domain Server', 'Domain Search', 'Hostname',
         'NETBIOS Name Srv', 'NETBIOS Scope', 'MTU Interface',
         'Classless Static Route Option', 'NTP Servers',
         'Reserved (Private Use)', 'Static Route', 'Reserved (Private Use)'],
    'dhcp_vendor': None,
    'dhcp_fp':
        [1, 28, 2, 3, 15, 6, 119, 12, 44, 47, 26, 121, 42, 249, 33, 252],
    'devices': ['Generic Linux'],
    'devices_mac': ['Generic Linux']
}


def test_write_md_report():
    outfpath = os.path.join('..', 'output.md')
    write_md_report(data, content, outfpath)
