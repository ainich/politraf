#!/usr/bin/env python3
# -*- coding: utf-8
import dbmodels
import datetime
import pyshark
import os
from pytz import timezone
import yaml

# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.load(stream))
        interface = config['interface']
        bpf_filter = config['bpf_filter']
        time_zone = config['time_zone'] 
    except yaml.YAMLError as e:
        print(e)

# PyShark config
cap = pyshark.LiveCapture(interface=interface, bpf_filter=bpf_filter)

db = dbmodels.Database('conn_stat')
#db.create_table(CONNStats)
tz = timezone(time_zone)


def print_conversation_header(pkt):
    try:
        protocol = pkt.transport_layer
        if protocol == "UDP" or protocol == "TCP":
            src_addr = pkt.ip.src
            src_port = pkt[pkt.transport_layer].srcport
            dst_addr = pkt.ip.dst
            dst_port = pkt[pkt.transport_layer].dstport

            # UDP traf
            if protocol == "UDP":
                # DNS request
                if "dns" in pkt:
                    if pkt.dns.qry_name:
                        qry_name = pkt.dns.qry_name
                else:
                    qry_name = "none"

            # TCP traf
            if protocol == "TCP":
                if "http.host" in pkt:
                    qry_name = pkt.http.host
                else:
                    qry_name = "none"
            
            timestamp = datetime.datetime.now(tz)
            today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
            #print (today, timestamp, protocol, src_addr, src_port, dst_addr, dst_port, qry_name)
            db.insert([
                dbmodels.CONNStats(event_date=today, timestamp=timestamp, protocol=protocol, src_addr=src_addr, src_port=src_port, dst_addr=dst_addr, dst_port=dst_port, qry_name=qry_name)
                ])
    except Exception as e:
        print(e)
        
if __name__ == '__main__':

    try:
        print ("Running tshark with: interface: "+interface+" and bpf_filter: "+bpf_filter)
        cap.apply_on_packets(print_conversation_header)
    except Exception as e:
        print(e)
        