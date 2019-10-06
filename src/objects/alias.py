#!/usr/bin/env python3

class Alias:
    def __init__(self, aliasfile):
        self.aliasfile = aliasfile

    def read_aliases(self):
        f = open(self.aliasfile)

        aliases = {}

        for line in f:
            if line.strip() == "" or line.startswith('#'):
                continue
            alias, prefix = line.split()
            aliases[prefix] = alias

        return aliases
