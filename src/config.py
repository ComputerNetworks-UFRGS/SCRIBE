#!/usr/bin/env python3

import json

def read_config(CONFIG_FILE):
    f = open(CONFIG_FILE)
    config = json.loads(f.read())
    return config
