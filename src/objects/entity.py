#!/usr/bin/env python3

class Entity:
    def __init__(self, src, dst, op):
        self.src = src
        self.dst = dst
        self.op = op

    def get_tuple(self):
        return (self.src, self.dst, self.op)