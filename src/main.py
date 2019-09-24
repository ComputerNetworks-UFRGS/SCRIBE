#!/usr/bin/env python3

import csv
import sys
import re
import os
import ipaddress

import config
from objects.port import Port
from firewall.filtering import Filtering
from translation.nile import Nile

def grouping(entities, filter_entities):
    for entity in filter_entities:
        k = (entity['src'], entity['dst'], entity['action'])
        if k not in entities:
            entities[(entity['src'], entity['dst'], entity['action'])] = [entity['traffic']]
        else:
            entities[k].append(entity['traffic'])

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

    nile = Nile(entities)
    output = nile.translation()

    print(output)
