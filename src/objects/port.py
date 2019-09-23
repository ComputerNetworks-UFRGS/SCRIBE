#!/usr/bin/env python3

import csv

PORT_DATABASE = '../databases/service-names-port-numbers.csv'

class Port:
    def __init__(self, port_number):
        self.port_number = port_number
        self.udpportservices = {}
        self.tcpportservices = {}
        self.name = ""

    def query(self, port, protocol = 'tcp'):
        if protocol == 'udp':
            return self.udpportservices[port]
        return self.tcpportservices[port]

    def read_ports(self):
        with open(PORT_DATABASE) as csvfile:
            portreader = csv.reader(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)

            ports = list(portreader)[1:]

            for port in ports:
                colcount = 0

                for colvalue in port:
                    if colcount == 0 and colvalue == '':
                        continue
                    if colcount == 2:
                        if colvalue == 'udp':
                            self.udpportservices[port[1]] = (port[0], port[3])
                        else:
                            self.tcpportservices[port[1]] = (port[0], port[3])

                    colcount += 1

    def detect_service_by_port(self):
        self.read_ports()
        if self.port_number == '*':
            self.name = 'all'
            return
        service = self.query(self.port_number)
        self.name = service[1]

    def get_name(self):
        return self.name