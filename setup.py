#!/usr/bin/python3
# -*- coding: utf-8
##############################################################################
# Politraf, initial setup
##############################################################################

import dbmodels
import shutil
import os
import yaml

try:
    print ("Make dir /etc/politraf")
    os.makedirs("/etc/politraf")
    print ("Copy config.yaml to /etc/politraf")
    shutil.copy2('config/config.yaml', '/etc/politraf/config.yaml')
    print ("Make dir /opt/politraf")
    os.makedirs("/opt/politraf")
    print ("Setup services")
    shutil.copy2('config/systat.service', '/etc/systemd/system/systat.service')
    shutil.copy2('config/constat.service', '/etc/systemd/system/constat.service')
    print ("Copy politraf files")
    shutil.copy2('systat.py', '/opt/politraf/systat.py')
    shutil.copy2('otxget.py', '/opt/politraf/otxget.py')
    shutil.copy2('constat.py', '/opt/politraf/constat.py')
    shutil.copy2('dbmodels.py', '/opt/politraf/dbmodels.py')
    os.makedirs("src")
    shutil.copy2('systat.py', 'src/systat.py')
    shutil.copy2('otxget.py', 'src/otxget.py')
    shutil.copy2('constat.py', 'src/constat.py')
    shutil.copy2('dbmodels.py', 'src/dbmodels.py')
    print ("Create database with tables")
    # Read config
    with open("config/config.yaml", 'r') as stream:
        try:
            config = (yaml.load(stream))
            url = config['db_url']
            name = config['username']
            passw = config['password']
        except Exception as e:
            print(e)
    # Create tables

    db = dbmodels.Database('politraf', db_url=url, username=name, password=passw, readonly=False, autocreate=True)
    db.create_table(dbmodels.CONNStats)
    db.create_table(dbmodels.CPUStats)
    db.create_table(dbmodels.MEMStats)
    db.create_table(dbmodels.DISKStats)
    db.create_table(dbmodels.IOCStats)
except Exception as e:
    print(e)