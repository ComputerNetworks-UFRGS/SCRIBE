#!/usr/bin/env python3

class Nile:
    def __init__(self, entities):
        self.entities = entities
        self.nile_symbols = {
            'src': 'from endpoint',
            'dst': 'to endpoint',
            'allow': 'allow protocol'
        }

    def process_entity(self, k, v):
        src, dst, action = k
        traffic = v
        return {
            'src': src,
            'dst': dst,
            'action': action,
            'traffic': traffic
        }

    def translation(self):
        nile_intent = ''
        for key in self.entities.keys():
            value = self.entities[key]
            entity = self.process_entity(key, value)
            nile_intent += self.translate_intent(entity) + '\n\n'
        return nile_intent

    def translate_intent(self, entity):
        nile_code = self.create_header()
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
        return mapped

    def create_header(self, intent_name='firewallIntent'):
        return 'define intent {}:'.format(intent_name)
