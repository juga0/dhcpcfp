#!/usr/bin/env python

#   This file is part of dhcpcfp, a set of scripts to
#   use different tor guards depending on the network we connect to.
#
#   Copyright (C) 2016 juga (juga at riseup dot net)
#
#   dhcpcfp is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License Version 3 of the
#   License, or (at your option) any later version.
#
#   dhcpcfp is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with dhcpcfp.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages
import dhcpcfp

setup(
    name='dhcpcfp',
    version=dhcpcfp.__version__,
    description=dhcpcfp.__description__,
    long_description=dhcpcfp.__long_description__,
    author=dhcpcfp.__author__,
    author_email=dhcpcfp.__author_mail__,
    license='GPLv3+',
    url=dhcpcfp.__website__,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'scapy>=2.2";python_version<="2.7"',
        'scapy-python3>=0.21;python_version>="3.4"',
        "pip>=8.1"
    ],
    extras_require={
        'dev': ['ipython', 'pyflakes', 'pep8'],
        'test': ['coverage', 'coveralls', 'codecov', 'tox', 'pytest'],
        'doc': ['sphinx', 'pylint']
    },
    entry_points={
        'console_scripts': [
            'dhcpcfp = dhcpcfp.dhcpcfp:main',
        ]
    },
    include_package_data=True,
    keywords='python scapy dhcp RFC7844 RFC2131 anonymity fingerprint',
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Environment :: Console",
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 ' +
        'or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
