#!/usr/bin/env python3
# -*- coding: utf-8
##############################################################################
# Politraf, initial setup
##############################################################################

import dbmodels
import yaml

# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.load(stream))
        url = config['db_url']
        name = config['username']
        passw = config['password']
    except yaml.YAMLError as e:
        print(e)

db = dbmodels.Database('politraf', db_url=url, username=name, password=passw, readonly=False, autocreate=True)
db.create_table(CONNStats)
db.create_table(CPUStats)
db.create_table(MEMStats)
db.create_table(DISKStats)
db.create_table(IOCStats)