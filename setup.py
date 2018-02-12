#!/usr/bin/python3.6
# -*- coding: utf-8
##############################################################################
# Politraf, initial setup
##############################################################################

import shutil
import os
import stat

import yaml

import dbmodels

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
    shutil.copy2('src/systat.py', '/opt/politraf/systat.py')
    shutil.copy2('src/otxget.py', '/opt/politraf/otxget.py')
    shutil.copy2('src/constat.py', '/opt/politraf/constat.py')
    shutil.copy2('src/ext_cscan.py', '/opt/politraf/ext_cscan.py')
    shutil.copy2('src/iocwatch.py', '/opt/politraf/iocwatch.py')
    shutil.copy2('dbmodels.py', '/opt/politraf/dbmodels.py')
    #os.chmod("src/systat.py", stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    #os.chmod("src/otxget.py", stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    #os.chmod("src/constat.py", stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    #os.chmod("src/dbmodels.py", stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
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
    db.create_table(dbmodels.OPEN_PORTS)
except Exception as e:
    print(e)
