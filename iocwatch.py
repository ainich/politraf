#!/usr/bin/env python3
# -*- coding: utf-8
##############################################################################
# Politraf, check connections for network IOC
##############################################################################


import dbmodels
import datetime
from pytz import timezone
import yaml
import time

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

db = dbmodels.Database('politraf', db_url=url, username=name, password=passw, readonly=False, autocreate=True)
tz = timezone(time_zone)

# 5 min time
to_time = datetime.datetime.now(tz)
from_time = (datetime.datetime.now(tz) - datetime.timedelta(minutes=1)).replace(microsecond=0)
from_time_epoch = str(from_time.timestamp())
today = datetime.datetime.strftime(datetime.datetime.now(tz), '%Y-%m-%d')

def get_traf_last():
        start = time.time()
        print ("Starting fetch traffic stat ...")
        for row in db.select('SELECT uniq(dst_addr), * FROM politraf.connstats WHERE timestamp >= toDateTime('+from_time_epoch+') GROUP BY dst_addr, event_date, timestamp, protocol, src_addr, src_port, dst_port, qry_name ORDER BY timestamp'):
            timestamp = datetime.datetime.now(tz)
            if not row.qry_name == 'none':
                for ioc in db.select('SELECT * FROM politraf.ioc_otx WHERE indicator = \''+row.qry_name+'\' ORDER BY timestamp'):
                    print (row.src_addr, row.src_port, row.dst_addr, row.dst_port, row.qry_name, ioc.name, ioc.indicator, ioc.references)
                    db.insert([
                    dbmodels.IOCStats(event_date=today, timestamp=timestamp, protocol=row.protocol, src_addr=row.src_addr, src_port=row.src_port, dst_addr=row.dst_addr, dst_port=row.dst_port, qry_name=row.qry_name, indicator=ioc.indicator, name=ioc.name, references=ioc.references)
                    ])    
            else:
                for ioc in db.select('SELECT * FROM politraf.ioc_otx WHERE indicator = \''+row.dst_addr+'\' ORDER BY timestamp'):
                    print (row.src_addr, row.src_port, row.dst_addr, row.dst_port, row.qry_name, ioc.name, ioc.indicator, ioc.references)
                    db.insert([
                    dbmodels.IOCStats(event_date=today, timestamp=timestamp, protocol=row.protocol, src_addr=row.src_addr, src_port=row.src_port, dst_addr=row.dst_addr, dst_port=row.dst_port, qry_name=row.qry_name, indicator=ioc.indicator, name=ioc.name, references=ioc.references)
                    ])    
        end = time.time()
        time_to_end = end - start
        print('Time to all events ', time_to_end)

if __name__ == '__main__':

    # Retrieve the events and store the IOCs
    # otx_receiver.get_iocs_last(int(args.l))
    get_traf_last()
