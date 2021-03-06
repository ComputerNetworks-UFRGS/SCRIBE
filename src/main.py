#!/usr/bin/env python3

import csv
import sys
import re
import os
import ipaddress

import config
from objects.port import Port
from objects.alias import Alias
from firewall.filtering import Filtering
from firewall.nat import NAT
from translation.nile import Nile

def grouping(entities, filter_entities):
    for entity in filter_entities:
        k = (entity['src'], entity['dst'], entity['action'])
        if k not in entities:
            entities[(entity['src'], entity['dst'], entity['action'])] = [entity['traffic']]
        else:
            entities[k].append(entity['traffic'])

def grouping_nat(entities, nat_entities):
    for entity in nat_entities:
        k = (entity['src'], entity['dst'], entity['action'])
        if k not in entities:
            entities[k] = [(entity['traffic'], entity['param'])]
        else:
            entities[k].append((entity['traffic'], entity['param']))

def aggregation(entities, aliasfile):
    alias = Alias(aliasfile)
    aliases = alias.read_aliases()
    for entity in entities:
        src, dst, action = entity
        traffic = entities[(src, dst, action)]
        del entities[(src, dst, action)]
        if src in aliases:
            src = aliases[src]
        if dst in aliases:
            dst = aliases[dst]

        for i in range(len(traffic)):
            t = traffic[i]

            if isinstance(t, tuple):
                proto, nat_addr = t
                if nat_addr in aliases:
                    nat_addr = aliases[nat_addr]
                traffic[i] = (proto, nat_addr)

        entities[(src, dst, action)] = traffic

def get_path(file):
    return '/'.join(file.split('/')[:-1]) + '/'
    
if __name__ == '__main__':
    configfile = sys.argv[1]
    rel_path = get_path(configfile)

    config = config.read_config(configfile)

    NETWORK_PREFIXES = [ipaddress.ip_network(network) for network in config['network_prefixes']]

    aliasfile = None
    if 'alias_file' in config:
        aliasfile = rel_path + config['alias_file']

    mfilter = None

    entities = {}

    for filter_file in config['filtering']:
        csvfile = open(rel_path+filter_file)

        mfilter = Filtering(csvfile, NETWORK_PREFIXES)
        mfilter.read_csv()
        filter_entities = mfilter.export_entities()

        grouping(entities, filter_entities)

    for nat_file in config['nat']:
        csvfile = open(rel_path + nat_file)

        mnat = NAT(csvfile, NETWORK_PREFIXES)
        mnat.read_csv()
        nat_entities = mnat.export_entities()

        grouping_nat(entities, nat_entities)

    aggregation(entities, aliasfile)

    nile = Nile(entities)
    output = nile.translation()

    print(output)
