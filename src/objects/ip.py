#!/usr/bin/env python3

import ipaddress

class IP:
    def __init__(self, address):
        self.address = address

    def convert(self):
        self.address = ipaddress.ip_address(self.address)

    def valid(self):
        try: 
            ipaddress.IPv4Address(self.address)
            return True
        except:
            return False

    def __str__(self):
        return str(self.address)