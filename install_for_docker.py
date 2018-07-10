#!/usr/bin/python3
# -*- coding: utf-8
##############################################################################
# Politraf, initial setup
##############################################################################

from subprocess import call
from subprocess import Popen
import shutil
import os
import time


green='\033[32m'
greene='\033[0m'
orange='\033[33m'
orangee='\033[0m'
blue='\033[34m'

try:
    print (green + "Install requirements" + greene)
    call(["apt-get", "install" , "tshark"])
    os.putenv("LC_ALL", "C")
    #Popen('export LC_ALL=C', shell=True, executable='/bin/bash')
    call(["pip3", "install" , "--upgrade", "six"])
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)

import dbmodels

try:
    print (green + 'Install Clickhouse plugin for Grafana' + greene)
    call(["grafana-cli", "plugins" , "install" , "vertamedia-clickhouse-datasource"])
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)

try:
    print (green + "Start Clickhouse and Grafana" + greene)
    call(["systemctl", "daemon-reload"])
    call(["service", "clickhouse-server" , "restart"])
    call(["service", "grafana-server" , "restart"])
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)

try:
    print (green +"Make dir /etc/politraf" + greene)
    os.makedirs("/etc/politraf")
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)
try:
    print (green +"Make dir /opt/politraf/current" + greene)
    os.makedirs("/opt/politraf/current")
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)
try:
    print (green +"Copy config.yaml to /etc/politraf" + greene)
    shutil.copy2('/politraf/config/config.yaml', '/etc/politraf/config.yaml')
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)
try:
    print (green + 'Make dir /opt/politraf' + greene)
    os.makedirs("/opt/politraf")
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)
try:
    print (green +'Setup services' + greene)
    shutil.copy2('/politraf/config/systat.service', '/etc/systemd/system/systat.service')
    shutil.copy2('/politraf/config/constat.service', '/etc/systemd/system/constat.service')
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)
try:
    print (green + 'Copy politraf files' + greene)
    shutil.copy2('/politraf/src/systat.py', '/opt/politraf/systat.py')
    shutil.copy2('/politraf/src/otxget.py', '/opt/politraf/otxget.py')
    shutil.copy2('/politraf/src/constat.py', '/opt/politraf/constat.py')
    shutil.copy2('/politraf/src/csv_load_to_db.py', '/opt/politraf/csv_load_to_db.py')
    shutil.copy2('/politraf/src/ext_cscan.py', '/opt/politraf/ext_cscan.py')
    shutil.copy2('/politraf/src/iocwatch.py', '/opt/politraf/iocwatch.py')
    shutil.copy2('/politraf/dbmodels.py', '/opt/politraf/dbmodels.py')
    shutil.copy2('/politraf/src/ioc_self_get.py', '/opt/politraf/ioc_self_get.py')
    shutil.copy2('/politraf/src/ioc_self_watch.py', '/opt/politraf/ioc_self_watch.py')
    shutil.copy2('/politraf/src/self_ioc_list.csv', '/opt/politraf/self_ioc_list.csv')
    #os.chmod("src/systat.py", stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    #os.chmod("src/otxget.py", stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    #os.chmod("src/constat.py", stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    #os.chmod("src/dbmodels.py", stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)
try:
    print (green + 'Wait for clickhouse init and create database with tables' + greene)
    time.sleep(20)
    # Create tables
    db = dbmodels.Database('politraf', db_url="http://127.0.0.1:8123/", username="default", password="", readonly=False, autocreate=True)
    db.create_table(dbmodels.CONNStats)
    db.create_table(dbmodels.CONNStats_buffer)
    db.create_table(dbmodels.CPUStats)
    db.create_table(dbmodels.MEMStats)
    db.create_table(dbmodels.DISKStats)
    db.create_table(dbmodels.IOCStats)
    db.create_table(dbmodels.OPEN_PORTS)
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)
