#!/usr/bin/python3
# -*- coding: utf-8 -*-
##############################################################################
# Politraf, IOC from OTX to clickhouse
##############################################################################
# Create an account and select your feeds
# https://otx.alienvault.com

import datetime
import logging

from OTXv2 import OTXv2
import yaml

import dbmodels

# Set logging level
logging.basicConfig(level = logging.INFO)


# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.safe_load(stream))
        OTX_KEY = config['otx_key']
        url = config['db_url']
        name = config['username']
        passw = config['password']
    except yaml.YAMLError as e:
        logging.error("Error.",e)
    logging.info("Config is OK")

# Init clickhouse
try:
    db = dbmodels.Database('politraf', db_url=url, username=name, password=passw, readonly=False, autocreate=True)
    db.drop_table(dbmodels.IOC_OTX)
    db.create_table(dbmodels.IOC_OTX)
except Exception as e:
    logging.error("Error.",e)


class OTXReceiver():

    def __init__(self, api_key):
        try:
            self.otx = OTXv2(api_key)
        except Exception as e:
            logging.error("Error.",e)

    def get_iocs_last(self):
        logging.info("Starting OTX feed download ...")
        try:
            self.events = self.otx.getall()
        except Exception as e:
            logging.error("Error.",e)
        logging.info("Download complete - %s events received" % len(self.events))

    def write_iocs(self):

        today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

        logging.info("Processing indicators ...")
        for event in self.events:
            try:
                for indicator in event["indicators"]:

                    try:
                        if indicator["type"] in ('domain', 'hostname', 'IPv4', 'IPv6', 'CIDR'):
                            indicator = indicator["indicator"]
                            name = event["name"]
                            if event["references"]:
                                references = event["references"][0]
                            else:
                                references = "None"
                            timestamp = datetime.datetime.now()
                            today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
                            db.insert([dbmodels.IOC_OTX(event_date=today, timestamp=timestamp, indicator=indicator, name=name, references=references)])
                    except Exception as e:
                        logging.error("Error.",e)
                        pass

            except Exception as e:
                logging.error("Error.",e)

def main():
    if len(OTX_KEY) != 64:
        print ("Set an API key in /etc/politraf/config.yaml. Go to https://otx.alienvault.com create an account and get your own API key")
        sys.exit(0)

    # Create a receiver
    otx_receiver = OTXReceiver(api_key=OTX_KEY)

    # Retrieve the events and store the IOCs
    otx_receiver.get_iocs_last()

    # Write IOC files
    otx_receiver.write_iocs()


if __name__ == '__main__':
    main()
