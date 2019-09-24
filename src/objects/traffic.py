#!/usr/bin/env python3

import ipaddress

class Traffic:
    def __init__(self, src, dst, networks):
        self.src = src
        self.dst = dst
        self.networks = networks

    def is_input(self):
        for network in self.networks:
            input_condition = self.src == '*' and (self.dst == network or self.dst in network)
            if input_condition:
                return input_condition
        return False
    
    def is_output(self):
        output_condition = False
        if self.dst == '*':
            for network in self.networks:
                if self.src == network:
                    output_condition = True
                if isinstance(self.src,ipaddress.IPv4Address) and self.src in network:
                    output_condition = True
        return output_condition

    def is_internal(self):
        internal_condition = False
        for network in self.networks:
            internal_condition = self.src in network and self.dst in network
        return internal_condition