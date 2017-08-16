content = """DHCP Client Fingerprint report
=========================================

Data that would not be send with a DHCP client that implements the Anonymity Profiles:

- BOOTP layer: $bootp_diff

- DHCP layer: $dhcp_diff

- DHCP layer: Parameter Request List: $dhcp_prl_names

Options used to guess device and operating system (do not show this to the user)""

- dhcp_fingerprint: $dhcp_fp
- vendor_id: $dhcp_vendor

Possible devices and operating systems guessed from the data sent in the DHCP requests:

$devices

Solutions to be less identifiable

- Windows 10 (desktop and mobile?): enable WiFi randomization...
- Linux: in a short future, use systemd DHCP client or dhcpcanon...
- Android: nothing at the moment
- Iphone: nothing at the moment
- MacOS: nothing at the moment
"""
