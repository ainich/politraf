#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
# -*- coding: utf-8 -*-
#
# Get-OTX-IOCs
# Retrieves IOCs from Open Threat Exchange
#
# Create an account and select your feeds
# https://otx.alienvault.com
import dbmodels
from OTXv2 import OTXv2
import re
import os
import sys
import traceback
import yaml
from pytz import timezone
from datetime import datetime, date, time

# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.load(stream))
        OTX_KEY = config['otx_key']
    except yaml.YAMLError as exc:
        print(exc)


db = Database('ioc')
db.drop_table(IOC_OTX)
db.create_table(IOC_OTX)
tz = timezone('Europe/Moscow')

class OTXReceiver():

    def __init__(self, api_key):
        self.otx = OTXv2(api_key)
        

    def get_iocs_last(self):
        print ("Starting OTX feed download ...")
        self.events = self.otx.getall()
        print ("Download complete - %s events received" % len(self.events))

    def write_iocs(self):

        today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

        print ("Processing indicators ...")
        for event in self.events:
            try:
                for indicator in event["indicators"]:

                    try:
                        
                        if indicator["type"] in ('domain', 'hostname', 'IPv4', 'IPv6', 'CIDR'):
                            indicator = indicator["indicator"]
                            name = event["name"]
                            references = event["references"][0]
                            #print (indicator, name, references)
                            timestamp = datetime.datetime.now()
                            today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
                            db.insert([IOC_OTX(event_date=today, timestamp=timestamp, indicator=indicator, name=name, references=references)])

                    except Exception as e:
                        pass

            except Exception as e:
                traceback.print_exc()

if __name__ == '__main__':

    if len(OTX_KEY) != 64:
        print ("Set an API key in script or via -k APIKEY. Go to https://otx.alienvault.com create an account and get your own API key")
        sys.exit(0)

    # Create a receiver
    otx_receiver = OTXReceiver(api_key=OTX_KEY)

    # Retrieve the events and store the IOCs
    # otx_receiver.get_iocs_last(int(args.l))
    otx_receiver.get_iocs_last()

    # Write IOC files
    otx_receiver.write_iocs()
