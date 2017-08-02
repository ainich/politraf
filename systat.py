#!/usr/bin/python
# -*- coding: utf-8
##############################################################################
# Politraf, system stat to clickhouse
##############################################################################

import dbmodels
import psutil, time
from pytz import timezone
import datetime
import yaml

# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.load(stream))
        time_zone = config['time_zone']
        url = config['db_url']
        name = config['username']
        passw = config['password']
    except yaml.YAMLError as e:
        print(e)

tz = timezone(time_zone)
db = dbmodels.Database('politraf', db_url=url, username=name, password=passw, readonly=False, autocreate=True)

if __name__ == '__main__':
    
    running = True
    while running:
        try:
            time.sleep(10)
            stats = psutil.cpu_percent(percpu=True)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            timestamp = datetime.datetime.now(tz)
            today = datetime.datetime.strftime(datetime.datetime.now(tz), '%Y-%m-%d')
            db.insert([
                dbmodels.CPUStats(event_date=today, timestamp=timestamp, cpu_id=cpu_id, cpu_percent=cpu_percent)
                for cpu_id, cpu_percent in enumerate(stats)
            ])
            db.insert([
                dbmodels.MEMStats(event_date=today, timestamp=timestamp, total=mem[0], used=mem[3])
            ])
            db.insert([
                dbmodels.DISKStats(event_date=today, timestamp=timestamp, total=disk[0], used=disk[1])
            ])
        except Exception as e:
            print(e)
            running = False
        