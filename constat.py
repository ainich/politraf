#!/usr/bin/env python3
# -*- coding: utf-8

import dbmodels
import pyshark
from datetime import datetime, date, time
import yaml

# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.load(stream))
        interface = config['interface']
        bpf_filter = config['bpf_filter']
    except yaml.YAMLError as exc:
        print(exc)

# PyShark config
cap = pyshark.LiveCapture(interface=interface, bpf_filter=bpf_filter)

db = dbmodels.Database('conn_stat')
#db.create_table(CONNStats)


def print_conversation_header(pkt):
    protocol = pkt.transport_layer
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
        if "SSL" in pkt:
            qry_name = "none"
        elif "HTTP" in pkt:
            qry_name = pkt.http.host
        else:
            qry_name = "none"
            
    timestamp = datetime.datetime.now()
    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    #print (today, timestamp, protocol, src_addr, src_port, dst_addr, dst_port, qry_name)
    db.insert([
        CONNStats(event_date=today, timestamp=timestamp, protocol=protocol, src_addr=src_addr, src_port=src_port, dst_addr=dst_addr, dst_port=dst_port, qry_name=qry_name)
        ])

if __name__ == '__main__':
    
    running = True
    while running:
        try:
            cap.apply_on_packets(print_conversation_header, packet_count=50)
        except Exception as e:
            print(e)
            running = False
        