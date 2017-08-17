.. _running:

Running dhcpcfp
==================

An updated command line usage description can be always obtained with::
    scripts/dhcpcanon -h

At the time of writing this the usage documentation is::

    usage: dhcpcfp [-h] [-v] [--version] [-f FINGERPRINT] [-e VENDOR]
                   [-i INTERFACE] [-m MAC] [-a] [-o OUTPUT] [-d DB] [-p PCAPFILE]
                   [-c]

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Set logging level to debug
      --version             version
      -f FINGERPRINT, --fingerprint FINGERPRINT
                            DHCP fingerprint.
      -e VENDOR, --vendor VENDOR
                            DHCP vendor.
      -i INTERFACE, --interface INTERFACE
                            Interface where to listen for DHCP.
      -m MAC, --mac MAC     MAC address to listen for DHCP traffic.
      -a, --all             Not recommended, use at your own risk.
      -o OUTPUT, --output OUTPUT
                            Report path.
      -d DB, --db DB        DB path with DHCP fingerprints.
      -p PCAPFILE, --pcapfile PCAPFILE
                            Obtain devices from pcap dump instead of scanning.
      -c, --continuous      Scan until user cancel.
