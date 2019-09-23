#!/usr/bin/env python3

import csv
import sys
import re
import config
import os
import ipaddress

sys.path.insert(0, os.path.abspath('..'))

from objects import port
from objects import ip
from firewall import filtering

def format_nile(entities):
    for k,v in entities.items():
        traffics = []
        _from, to, op = k
        print("define intent firewallIntent:")
        print("\tfrom endpoint ('"+_from+"')")
        print("\tto endpoint ('"+to+"')")
        for traffic in v:
             traffics.append(traffic)
        if len(traffics) >= 1:
            if op == 'allow':
                print("\tallow ",end='')
                for t in traffics:
                    print("protocol ('"+traffic+"'), ", end='')
            elif op == 'forward':
                nat_dst, action = v 
                print("\tfor protocol ('"+traffic[0]+"')")
                print("\tforward address ('"+nat_dst+"')")
        print("\n")

def detect_traffic_by_port(port_number):
    port = Port()
    port.read_ports('databases/service-names-port-numbers.csv')
    if port_number == '*':
        return 'all'
    service = port.query(port_number)
    return service[1]

def get_path(file):
    return '/'.join(file.split('/')[:-1]) + '/'
    
if __name__ == '__main__':
    configfile = sys.argv[1]
    rel_path = get_path(configfile)

    config = config.read_config(configfile)

    NETWORK_PREFIX = ipaddress.ip_network(config['network_prefix'])

    aliasfile = None
    if 'alias_file' in config:
        aliasfile = rel_path + config['alias_file']

    mfilter = None

    entities = {}

    for filter_file in config['filtering']:
        csvfile = open(rel_path+filter_file)

        mfilter = filtering.Filtering(csvfile, NETWORK_PREFIX)

        mfilter.read_csv()
        mentities = mfilter.export_entities()
        for e in mentities:
            k = (e['src'], e['dst'], e['action'])
            if k not in entities:
                entities[(e['src'], e['dst'], e['action'])] = [e['traffic']]
            else:
                entities[k].append(e['traffic'])



    if mfilter:
        format_nile(entities)