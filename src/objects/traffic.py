#!/usr/bin/env python3

import ipaddress

class Traffic:
    def __init__(self, src, dst, network):
        self.src = src
        self.dst = dst
        self.network = network

    def is_input(self):
        return self.src == '*' and (self.dst == self.network or self.dst in self.network)
    
    def is_output(self):
        if self.dst == '*':
            if self.src == self.network:
                return True
            if isinstance(self.src,ipaddress.IPv4Address) and self.src in self.network:
                return True

    def is_internal(self):
        return self.src in self.network and self.dst in self.network