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

from string import Template

def write_md_report(data, content, outfpath):
    logger.debug('data %s', data)
    template = Template(content)
    logger.debug('template %s', template)
    report = template.substitute(**data)
    with io.open(outfpath, 'wb') as fd:
        fd.write(report)
