# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
# Copyright 2016, 2017 juga (juga at riseup dot net), MIT license.
"""Logging configuration."""
import logging
import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'ColoredFormatter': {},
    'formatters': {
        'verbose_color': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s %(levelname)s'
                      ' %(filename)s:%(lineno)s -'
                      ' %(funcName)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple_color': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(message)s'
        },
        'verbose': {
            'format': '%(asctime)s %(levelname)s'
                      ' %(filename)s:%(lineno)s -'
                      ' %(funcName)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': "%(message)s",
        },
        'sys': {
            'format': "%(module)s[%(process)s]: "
                      "%(message)s"
        }
    },
    'handlers': {
        'stdout': {
            'class': 'colorlog.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple_color',
            'level': 'DEBUG',
        },
        'stdoutscapy': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple',
            'level': 'INFO',
        },
        'syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
            'formatter': 'sys',
            'level': 'INFO',
        },
    },
    'loggers': {
        'dhcpcfp': {
            'handlers': ['syslog', 'stdout'],
            'level': logging.INFO,
            'propagate': False
        },
        "scapy": {
            'handlers': ['stdoutscapy'],
            'level': logging.INFO,
            'propagate': False
        },
        "scapy.interactive": {
            'handlers': ['stdoutscapy'],
            'level': logging.INFO,
            'propagate': False
        }
    }
}
