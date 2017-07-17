#!/usr/bin/python3
# -*- coding: utf-8
import pyshark
import os
import glob
from infi.clickhouse_orm import models, fields, engines
from pytz import timezone
from datetime import datetime, date, time
from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import MergeTree
import yaml

with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.load(stream))
        interface = config['interface']
        bpf_filter = config['bpf_filter']
    except yaml.YAMLError as exc:
        print(exc)

# PyShark config
cap = pyshark.LiveCapture(interface=interface, bpf_filter=bpf_filter)

class CONNStats(Model):

    event_date = DateField()
    timestamp = DateTimeField()
    protocol = StringField()
    src_addr = StringField()
    src_port = Float32Field()
    dst_addr = StringField()
    dst_port = Float32Field()
    qry_name = StringField()
    
    engine = MergeTree('event_date', ('timestamp', 'protocol', 'src_addr', 'src_port', 'dst_addr', 'dst_port', 'qry_name'))

db = Database('conn_stat')
db.create_table(CONNStats)
tz = timezone('Europe/Moscow')


def print_conversation_header(pkt):
    protocol = pkt.transport_layer
    src_addr = pkt.ip.src
    src_port = pkt[pkt.transport_layer].srcport
    dst_addr = pkt.ip.dst
    dst_port = pkt[pkt.transport_layer].dstport

    # UDP traf
    if protocol == "UDP":
        # DNS request
        if pkt.dns.qry_name:
            qry_name = pkt.dns.qry_name
        elif pkt.dns.resp_name:
            qry_name = pkt.dns.resp_name

    # TCP traf
    else:
        if "SSL" in pkt:
            qry_name = "none"
            
        elif "HTTP" in pkt:
            qry_name = pkt.http.host
            
        else:
            qry_name = "none"

    timestamp = datetime.datetime.now(tz)
    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    #print (today, timestamp, protocol, src_addr, src_port, dst_addr, dst_port, qry_name)
    db.insert([
        CONNStats(event_date=today, timestamp=timestamp, protocol=protocol, src_addr=src_addr, src_port=src_port, dst_addr=dst_addr, dst_port=dst_port, qry_name=qry_name)
        ])


while True:
    # Define tmp pcap
    #tmpfiles = glob.glob('/tmp/wireshark*')
    #for f in tmpfiles:
    #    os.remove(f)
    try:
        cap.apply_on_packets(print_conversation_header)

    except Exception as e:
        print(e)
        break
        