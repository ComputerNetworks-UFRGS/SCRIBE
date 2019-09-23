#!/usr/bin/env python3

from traffic import Traffic

class NATTraffic(Traffic):
    def __init__(self, src, dst, network, nat_src, nat_dst):
        Traffic.__init__(src, dst, network)
        self.nat_src = nat_src
        self.nat_dst = nat_dst

    def is_nat_input(self):
        return self.src == '*' and self.nat_dst in self.network