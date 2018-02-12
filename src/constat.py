#!/usr/bin/python3
# -*- coding: utf-8
##############################################################################
# Politraf, connections to clickhouse
##############################################################################

import datetime
#import os
#import psutil
#import time
import logging

import pyshark
import pytz
import yaml

import dbmodels

# Set logging level
logging.basicConfig(level = logging.INFO)


# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.safe_load(stream))
        interface = config['interface']
        interfaces = interface.split(",")
        bpf_filter = config['bpf_filter']
        time_zone = config['time_zone']
        tz = time_zone
        url = config['db_url']
        name = config['username']
        passw = config['password']
    except yaml.YAMLError as e:
        logging.error("Error." , e)
    logging.info("Config is OK")


# PyShark config
try:
    cap = pyshark.LiveCapture(interface=interfaces, bpf_filter=bpf_filter)
except Exception as e:
    logging.error("Error.",e)


# Init clickhouse
try:
    db = dbmodels.Database('politraf', db_url=url, username=name, password=passw, readonly=False, autocreate=True)
except Exception as e:
    logging.error("Error.",e)


def database_write(today, timestamp, protocol, src_addr, src_port, dst_addr, dst_port, qry_name):
    try:
        db.insert([
            dbmodels.CONNStats(event_date=today, timestamp=timestamp, protocol=protocol, src_addr=src_addr, src_port=src_port, dst_addr=dst_addr, dst_port=dst_port, qry_name=qry_name)
            ])
    except Exception as e:
        logging.error("Error.",e)


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
            local = pytz.timezone(tz)
            timestamp = local.localize(datetime.datetime.now())
            today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

            database_write(today, timestamp, protocol, src_addr, src_port, dst_addr, dst_port, qry_name)

    except Exception as e:
        logging.error("Error.",e)


def main():
    try:
        logging.info("Running tshark with: interface: "+interface+" and bpf_filter: "+bpf_filter+ " and send connections stats to clickhouse")
        cap.apply_on_packets(print_conversation_header)
    except Exception as e:
        logging.error("Error.",e)
if __name__ == '__main__':
    main()
