#!/usr/bin/python3
# -*- coding: utf-8 -*-
##############################################################################
# Politraf, IOC from file to clickhouse
##############################################################################

import datetime
import logging
import csv
import os
import time

import yaml

import dbmodels

# Set logging level
logging.basicConfig(level = logging.ERROR)


# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.safe_load(stream))
        OTX_KEY = config['otx_key']
        TRAF_FILE = config['traf_file']
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


class TReceiver():

    def __init__(self, traf_file):
        try:
            self.gs = traf_file
        except Exception as e:
            logging.error(e)

    def write_traf(self):
        start = time.time()
        logging.info("Processing traffic ...")
        with open(self.gs, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            os.remove(self.gs)
            for event in spamreader:
                try:
                    today = event[0]
                    timestamp = event[1]
                    protocol = event[2]
                    src_addr = event[3]
                    src_port = event[4]
                    dst_addr = event[5]
                    dst_port = event[6]
                    qry_name = event[7]
                    db.insert([dbmodels.CONNStats_buffer(event_date=today, timestamp=timestamp, protocol=protocol, src_addr=src_addr, src_port=src_port, dst_addr=dst_addr, dst_port=dst_port, qry_name=qry_name)])

                except Exception as e:
                    logging.error(e)
        #os.remove(self.gs)
        end = time.time()
        time_to_end = end - start
        print('Time to load traffic ', time_to_end)

def main():

    # Create a receiver
    t_receiver = TReceiver(traf_file=TRAF_FILE)

    # Write IOC files
    t_receiver.write_traf()


if __name__ == '__main__':
    main()
