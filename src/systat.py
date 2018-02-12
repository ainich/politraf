#!/usr/bin/python3
# -*- coding: utf-8
##############################################################################
# Politraf, system stat to clickhouse
##############################################################################

import datetime
import psutil
import time
import logging

from pytz import timezone
import yaml

import dbmodels


# Set logging level
logging.basicConfig(level = logging.INFO)


# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.safe_load(stream))
        time_zone = config['time_zone']
        tz = timezone(time_zone)
        url = config['db_url']
        name = config['username']
        passw = config['password']
    except yaml.YAMLError as e:
        logging.error(e)
    logging.info("Config is OK")

# Init clickhouse
try:
    db = dbmodels.Database('politraf', db_url=url, username=name, password=passw, readonly=False, autocreate=True)
except Exception as e:
    logging.error(e)

def database_write(stats, mem, disk, timestamp, today):
    try:
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
        logging.error(e)

def main():
    logging.info("Starting send system stats to clickhouse")
    running = True
    while running:
        try:
            time.sleep(10)
            stats = psutil.cpu_percent(percpu=True)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            timestamp = datetime.datetime.now(tz)
            today = datetime.datetime.strftime(datetime.datetime.now(tz), '%Y-%m-%d')
            database_write(stats, mem, disk, timestamp, today)

        except Exception as e:
            print(e)
            running = False

if __name__ == '__main__':
    main()        