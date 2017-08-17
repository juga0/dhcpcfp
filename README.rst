dhcpcfp - DHCP client fingerprint
=================================

|PyPI| |Build Status| |Coverage Status|

Detect your own DHCP fingerprint.

``dhcpcfp`` scans the DHCP client REQUEST packet and creates a report
with the fingerprinting data found, the differences of that data with
``dhcpcanon`` and how to avoid to be fingerprinted through DHCP.

Documentation
-------------

A more extensive online documentation is available in `Read the
docs <https://dhcpcfp.readthedocs.io/>`__. The documentation source is
in `this repository <docs/source/>`__.

Visit `DHCPAP <https://github.com/dhcpap>`__ for an overview of all the
repositories related to the RFC7844 implementation work.

Installation
------------

See `Installation <docs/source/install.rst>`__

Download
--------

You can download this project in either
`zip <http://github.com/juga0/dhcpcfp/zipball/master()>`__ or
`tar <http://github.com/juga0/dhcpcfp/tarball/master>`__ formats.

You can also clone the project with Git by running:

git clone https://github.com/juga0/dhcpcfp

Bugs and features
-----------------

If you wish to signal a bug or report a feature request, please fill-in
an issue on the `dhcpcfp issue
tracker <https://github.com/juga0/dhcpcfp/issues>`__.

Current status
--------------

WIP

License
-------

dhcpcfp is Copyright 2017 by juga ( juga at riseup dot net), and is
covered by the [|GPLv3|] (http://www.gnu.org/licenses/) license.

Acknowledgments
---------------

To the persons that have given suggestions and comments about this
implementation.

.. |GPLv3| image:: https://www.gnu.org/graphics/gplv3-127x51.png
.. |PyPI| image:: https://img.shields.io/pypi/v/dhcpcfp.svg
   :target: https://pypi.python.org/pypi/dhcpcfp
.. |Build Status| image:: https://www.travis-ci.org/juga0/dhcpcfp.svg?branch=master
   :target: https://www.travis-ci.org/juga0/dhcpcfp
.. |Coverage Status| image:: https://coveralls.io/repos/github/juga0/dhcpcfp/badge.svg?branch=master
   :target: https://coveralls.io/github/juga0/dhcpcfp?branch=master
