#!/usr/bin/env python3

class Nile:
    def __init__(self, entities):
        self.entities = entities
        self.intent_number = 1
        self.nile_symbols = {
            'src': 'from endpoint',
            'dst': 'to endpoint',
            'for': 'for traffic',
            'allow': 'allow protocol',
            'forward': 'forward address'
        }

    def extract_params(self, v):
        traffic = []
        params = []
        for entity in v:
            t = entity
            if isinstance(entity, tuple):
                t, p = entity
                params.append(p)
            traffic.append(t)
        return (traffic, params)

    def process_entity(self, k, v):
        src, dst, action = k        
        traffic, params = self.extract_params(v)

        return {
            'src': src,
            'dst': dst,
            'action': action,
            'traffic': traffic,
            'params': params
        }

    def translation(self):
        nile_intent = ''
        for key in self.entities.keys():
            value = self.entities[key]
            entity = self.process_entity(key, value)
            nile_intent += self.translate_intent(entity)
        return nile_intent

    def translate_intent(self, entity):
        nile_code = ""
        if(entity['params']):
            for i in range(len(entity['params'])):
                param = entity['params'][i]
                traffic = entity['traffic'][i]
                nile_code += self.create_header()
                nile_code += self.append_target(entity)
                nile_code += self.nile_map_params(entity['action'], traffic, param)
        else:
            nile_code += self.create_header()
            nile_code += self.append_target(entity)
            nile_code += self.nile_map_traffic(entity['action'], entity['traffic'])
        return nile_code

    def append_target(self, entity):
        nile_target = self.nile_map('src', entity['src'])
        nile_target += self.nile_map('dst', entity['dst'])
        return nile_target

    def nile_map(self, key, value):
        return "\n\t{} ('{}')".format(self.nile_symbols[key], value)
    
    def nile_map_traffic(self, key, values):
        mapped = "\n\t{} ('{}')".format(self.nile_symbols[key], values[0])
        for value in values[1:]:
            mapped += ", ('{}')".format(value)
        return mapped + '\n\n'
    
    def nile_map_params(self, key, traffic, target):
        mapped = "\n\t{} ('{}')".format(self.nile_symbols['for'], traffic)
        mapped += "\n\t{} ('{}')\n\n".format(self.nile_symbols[key], target)
        return mapped

    def create_header(self, intent_name='firewallIntent'):
        header = 'define intent {}{}:'.format(intent_name, self.intent_number)
        self.intent_number += 1
        return header
