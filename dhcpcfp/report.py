# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
# Copyright 2016 juga <juga@riseup.net>
# This file is part of dhcpcfp.
"""."""
import io
import logging
from string import Template

logger = logging.getLogger('dhcpcfp')


def write_md_report(data, content, outfpath, continuous=False):
    logger.debug('data %s', data)
    template = Template(content)
    logger.debug('template %s', template)
    report = template.substitute(**data)
    if continuous:
        with io.open(outfpath, 'ab') as fd:
            fd.write(report)
    else:
        with io.open(outfpath, 'wb') as fd:
            fd.write(report)
