#!/usr/bin/python3
# -*- coding: utf-8
##############################################################################
# Politraf, check connections for network IOC
##############################################################################


import time
import datetime
import logging

from pytz import timezone
import yaml

import dbmodels


# Set logging level
logging.basicConfig(level = logging.ERROR)


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


# 5 min time
to_time = datetime.datetime.now(tz)
from_time = (datetime.datetime.now(tz) - datetime.timedelta(minutes=1)).replace(microsecond=0)
from_time_epoch = str(from_time.timestamp())
today = datetime.datetime.strftime(datetime.datetime.now(tz), '%Y-%m-%d')

def get_traf_last():
        try:
            start = time.time()
            logging.info("Starting fetch traffic stat ...")
            for row in db.select(
                    'SELECT dst_addr, src_addr, qry_name, protocol, src_port, dst_port FROM politraf.connstats WHERE timestamp >= toDateTime(' + from_time_epoch + ') GROUP BY dst_addr, src_addr, qry_name, protocol, src_port, dst_port'):
                for ioc in db.select('SELECT * FROM politraf.ioc_otx WHERE indicator = \''+row.qry_name+'\' ORDER BY timestamp'):
                    db.insert([dbmodels.IOCStats(event_date=today, timestamp=to_time, protocol=row.protocol, src_addr=row.src_addr, src_port=row.src_port, dst_addr=row.dst_addr, dst_port=row.dst_port, qry_name=row.qry_name, indicator=ioc.indicator, name=ioc.name, references=ioc.references)])
                for ioc in db.select('SELECT * FROM politraf.ioc_otx WHERE indicator = \''+row.dst_addr+'\' ORDER BY timestamp'):
                    db.insert([
                        dbmodels.IOCStats(event_date=today, timestamp=to_time, protocol=row.protocol, src_addr=row.src_addr, src_port=row.src_port, dst_addr=row.dst_addr, dst_port=row.dst_port, qry_name=row.qry_name, indicator=ioc.indicator, name=ioc.name, references=ioc.references)
                        ])
            end = time.time()
            time_to_end = end - start
            print('Time to all events ', time_to_end)
        except Exception as e:
            logging.error(e)


def main():
    # Retrieve the events and store the IOCs
    get_traf_last()

if __name__ == '__main__':
    main()