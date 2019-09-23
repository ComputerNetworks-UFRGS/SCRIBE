#!/usr/bin/env python3

import csv
import re

from objects import ip
from objects import traffic
from objects import entity
from objects import port

class Filtering:
    def __init__(self, csvfile, NETWORK_PREFIX):
        self.csvinput = csvfile
        self.NETWORK_PREFIX = NETWORK_PREFIX
        self.rules = None
        self.aliases = None

    def read_csv(self):
        rulereader = csv.reader(self.csvinput, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)

        rulelist = list(rulereader)
        header = rulelist[0]
        rules = rulelist[1:]

        for i in range(len(rules)):
            if rules[i][0] == '':
                for k in range(len(rules[i])):
                    if rules[i][k] == '':
                        rules[i][k] = rules[i-1][k]

        self.rules = rules

    def generate_entity(self, src, dst, op, traffic):
        return {
            'src': src, 
            'dst': dst, 
            'action': op, 
            'traffic': traffic
        }

    def export_entities(self):
        entities = []
        for rule in self.rules:
            src_ip = ip.IP(rule[0])
            if(src_ip.valid()):
                src_ip.convert()
            dst_ip = ip.IP(rule[6])
            if(dst_ip.valid()):
                dst_ip.convert()

            traffic_classification = traffic.Traffic(src_ip.address, dst_ip.address, self.NETWORK_PREFIX)

            if traffic_classification.is_input():
                port_obj = port.Port(rule[7])
                port_obj.detect_service_by_port()
                service_name = port_obj.get_name()
                entities.append(self.generate_entity('internet', rule[6], 'allow', service_name))

            elif traffic_classification.is_output():
                port_obj = port.Port(rule[7])
                port_obj.detect_service_by_port()
                service_name = port_obj.get_name()
                entities.append(self.generate_entity(rule[0], 'internet', 'allow', service_name))

        return entities
