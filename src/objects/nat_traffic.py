#!/usr/bin/env python3

import ipaddress
from objects.traffic import Traffic

class NATTraffic(Traffic):
    def __init__(self, src, dst, networks, nat_src, nat_dst):
        Traffic.__init__(self,src, dst, networks)
        self.nat_src = nat_src
        self.nat_dst = nat_dst

    def is_nat_input(self):
        input_nat_condition = False
        for network in self.networks:
             input_nat_condition = self.src == '*' and (isinstance(self.nat_dst,ipaddress.IPv4Address) and self.nat_dst in network)
        return input_nat_condition
    
    def is_nat_output(self):
        return self.dst == '*' and self.nat_src in self.network