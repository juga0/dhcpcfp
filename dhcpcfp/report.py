# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
# Copyright 2016 juga <juga@riseup.net>
# This file is part of dhcpcfp.
"""."""
import io
import logging
from string import Template

from .conflog import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('dhcpcfp')


def write_md_report(data, content, outfpath):
    logger.debug('data %s', data)
    template = Template(content)
    logger.debug('template %s', template)
    report = template.substitute(**data)
    with io.open(outfpath, 'wb') as fd:
        fd.write(report)
