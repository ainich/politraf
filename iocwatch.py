#!/usr/bin/env python3
# -*- coding: utf-8

import dbmodels
import datetime


db = dbmodels.Database('ioc')
#db.create_table(IOCStats)

# 5 min time
to_time = datetime.datetime.now()
from_time = (datetime.datetime.now() - datetime.timedelta(minutes=5)).replace(microsecond=0)
from_time_epoch = str(from_time.timestamp())
today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

def get_traf_last():
        print ("Starting fetch traffic stat ...")
        for row in db.select('SELECT * FROM conn_stat.connstats WHERE timestamp >= toDateTime('+from_time_epoch+') ORDER BY timestamp'):
            #print (row.timestamp, row.src_addr, row.dst_addr, type(row.dst_addr))
            timestamp = datetime.datetime.now()
            if not row.qry_name == 'none':
                for ioc in db.select('SELECT * FROM ioc.ioc_otx WHERE indicator = \''+row.qry_name+'\' ORDER BY timestamp'):
                    print (row.src_addr, row.src_port, row.dst_addr, row.dst_port, row.qry_name, ioc.name, ioc.indicator, ioc.references)
                    db.insert([
                    IOCStats(event_date=today, timestamp=timestamp, protocol=row.protocol, src_addr=row.src_addr, src_port=row.src_port, dst_addr=row.dst_addr, dst_port=row.dst_port, qry_name=row.qry_name, indicator=ioc.indicator, name=ioc.name, references=ioc.references)
                    ])    
            else:
                for ioc in db.select('SELECT * FROM ioc.ioc_otx WHERE indicator = \''+row.dst_addr+'\' ORDER BY timestamp'):
                    print (row.src_addr, row.src_port, row.dst_addr, row.dst_port, row.qry_name, ioc.name, ioc.indicator, ioc.references)
                    db.insert([
                    IOCStats(event_date=today, timestamp=timestamp, protocol=row.protocol, src_addr=row.src_addr, src_port=row.src_port, dst_addr=row.dst_addr, dst_port=row.dst_port, qry_name=row.qry_name, indicator=ioc.indicator, name=ioc.name, references=ioc.references)
                    ])    


if __name__ == '__main__':

    # Retrieve the traffic events
    #traf_receiver = OTXWatch()

    # Retrieve the events and store the IOCs
    # otx_receiver.get_iocs_last(int(args.l))
    get_traf_last()
