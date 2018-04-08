#!/usr/bin/python3
# -*- coding: utf-8
##############################################################################
# Politraf, connections to clickhouse
##############################################################################

import datetime
#import os
#import psutil
import time
import logging
import requests
import csv

import pyshark
import pytz
import yaml

import dbmodels

# Set logging level
logging.basicConfig(level = logging.ERROR)


# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.safe_load(stream))
        TRAF_FILE = config['traf_file']
        interface = config['interface']
        interfaces = interface.split(",")
        bpf_filter = config['bpf_filter']
        time_zone = config['time_zone']
        tz = time_zone
        url = config['db_url']
        name = config['username']
        passw = config['password']
    except yaml.YAMLError as e:
        logging.error(e)
    logging.info("Config is OK")


# PyShark config
try:
    cap = pyshark.LiveCapture(interface=interfaces, bpf_filter=bpf_filter)
except Exception as e:
    logging.error(e)


# Init clickhouse
try:
    db = dbmodels.Database('politraf', db_url=url, username=name, password=passw, readonly=False, autocreate=True)
except Exception as e:
    logging.error(e)


def database_write(today, timestamp, protocol, src_addr, src_port, dst_addr, dst_port, qry_name):
    try:
        db.insert([
            dbmodels.CONNStats_buffer(event_date=today, timestamp=timestamp, protocol=protocol, src_addr=src_addr, src_port=src_port, dst_addr=dst_addr, dst_port=dst_port, qry_name=qry_name)
            ])
    except Exception as e:
        logging.error(e)

def database_write_bulk(data_buffer):
    try:
        start = time.time()
        db.insert(data_buffer)
        end = time.time()
        time_to_end = end - start
        print('Time to send all events ', time_to_end)
    except Exception as e:
        logging.error(e)

def csv_file_write(today, timestamp, protocol, src_addr, src_port, dst_addr, dst_port, qry_name):
    today=str(today)
    timestamp=str(timestamp)
    protocol=str(protocol)
    src_addr=str(src_addr)
    src_port=str(src_port)
    dst_addr=str(dst_addr)
    dst_port=str(dst_port)
    qry_name=str(qry_name)
    with open('/opt/politraf/current/traff.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([today, timestamp, protocol, src_addr, src_port, dst_addr, dst_port, qry_name])

def print_conversation_header(pkt):
    try:
        start = time.time()
        protocol = pkt.transport_layer

        src_addr = pkt.ip.src
        src_port = pkt[pkt.transport_layer].srcport
        dst_addr = pkt.ip.dst
        dst_port = pkt[pkt.transport_layer].dstport
        qry_name = "none"

        # UDP traf
        if protocol == "UDP":
        # DNS request
            if "dns" in pkt:
                if pkt.dns.qry_name:
                    qry_name = pkt.dns.qry_name
        # TCP traf
        if protocol == "TCP":
            if "http.host" in pkt:
                qry_name = pkt.http.host

        local = pytz.timezone(tz)
        timestamp = local.localize(datetime.datetime.now())
        today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

        # prepare data for bulk
        data_buffer = []
        insert_data = dbmodels.CONNStats_buffer(
            event_date=today,
            timestamp=timestamp,
            protocol=protocol,
            src_addr=src_addr,
            src_port=src_port,
            dst_addr=dst_addr,
            dst_port=dst_port,
            qry_name=qry_name
            )
        # appends data into couple
        #data_buffer.append(insert_data)
        #database_write_bulk(data_buffer)
        csv_file_write(today, timestamp, protocol, src_addr, src_port, dst_addr, dst_port, qry_name)
        #print(today, timestamp, protocol, src_addr, src_port, dst_addr, dst_port, qry_name)
        #print(str(insert_data))
        end = time.time()
        time_to_end = end - start
        #print('Time to analyze packet ', time_to_end)

        #database_write_bulk(data_buffer)
        #print(data_buffer, insert_data)

    except Exception as e:
        logging.error(e)


def main():
    try:
        logging.info("Running tshark with: interface: "+interface+" and bpf_filter: "+bpf_filter+ " and send connections stats to clickhouse")
        cap.apply_on_packets(print_conversation_header)
        #cap.sniff(timeout=1)
        #var = 1
        #while var == 1:
        #    for pkt in cap.sniff_continuously(packet_count=4):
        #        print_conversation_header(pkt)
        #        cap.close()

    except Exception as e:
        logging.error(e)
if __name__ == '__main__':
    main()
