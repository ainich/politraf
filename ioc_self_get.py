#!/usr/bin/python3
# -*- coding: utf-8 -*-
##############################################################################
# Politraf, IOC from file to clickhouse
##############################################################################

import datetime
import logging
import csv

import yaml

import dbmodels

# Set logging level
logging.basicConfig(level = logging.INFO)


# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.safe_load(stream))
        OTX_KEY = config['otx_key']
        IOC_FILE = config['ioc_file']
        url = config['db_url']
        name = config['username']
        passw = config['password']
    except yaml.YAMLError as e:
        logging.error(e)
    logging.info("Config is OK")

# Init clickhouse
try:
    db = dbmodels.Database('politraf', db_url=url, username=name, password=passw, readonly=False, autocreate=True)
    db.drop_table(dbmodels.IOC_SELF)
    db.create_table(dbmodels.IOC_SELF)
except Exception as e:
    logging.error(e)


class GSReceiver():

    def __init__(self, ioc_file):
        try:
            self.gs = ioc_file
        except Exception as e:
            logging.error(e)

    def write_iocs(self):

        logging.info("Processing indicators ...")
        with open(self.gs, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for event in spamreader:
                try:
                    indicator = event[0]
                    if event[1]:
                        references = event[1]
                    else:
                        references = "None"
                    timestamp = datetime.datetime.now()
                    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
                    db.insert([dbmodels.IOC_SELF(event_date=today, timestamp=timestamp, indicator=indicator, name=name, references=references)])

                except Exception as e:
                    logging.error(e)

def main():

    # Create a receiver
    gs_receiver = GSReceiver(ioc_file=IOC_FILE)

    # Write IOC files
    gs_receiver.write_iocs()


if __name__ == '__main__':
    main()