#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
# -*- coding: utf-8 -*-
#
# Get-OTX-IOCs
# Retrieves IOCs from Open Threat Exchange
#
# Create an account and select your feeds
# https://otx.alienvault.com

from OTXv2 import OTXv2
import re
import os
import sys
import traceback
import argparse
import yaml
from infi.clickhouse_orm import models, fields, engines
from pytz import timezone
from datetime import datetime, date, time
from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import MergeTree

# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.load(stream))
        OTX_KEY = config['otx_key']
    except yaml.YAMLError as exc:
        print(exc)

class IOC_OTX(Model):

    event_date = DateField()
    timestamp = DateTimeField()
    indicator = StringField()
    name = StringField()
    references = StringField()
    
    engine = MergeTree('event_date', ('timestamp', 'indicator', 'name', 'references'))

db = Database('ioc')
db.create_table(IOC_OTX)
tz = timezone('Europe/Moscow')


class WhiteListedIOC(Exception): pass

class OTXReceiver():

    # IOC Strings
    hash_iocs = ""
    filename_iocs = ""
    c2_iocs = ""

    # Output format
    separator = ";"
    use_csv_header = False
    extension = "txt"
    hash_upper = False
    filename_regex_out = True

    def __init__(self, api_key, siem_mode, debug, proxy):
        self.debug = debug
        self.otx = OTXv2(api_key, proxy)
        if siem_mode:
            self.separator = ","
            self.use_csv_header = True
            self.extension = "csv"
            self.hash_upper = True
            self.filename_regex_out = False

    def get_iocs_last(self):
        # mtime = (datetime.now() - timedelta(days=days_to_load)).isoformat()
        print ("Starting OTX feed download ...")
        self.events = self.otx.getall()
        print ("Download complete - %s events received" % len(self.events))
        # json_normalize(self.events)

    def write_iocs(self, ioc_folder):

        today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

        print ("Processing indicators ...")
        for event in self.events:
            try:
                for indicator in event["indicators"]:

                    try:
#                        if indicator["type"] in ('FileHash-MD5', 'FileHash-SHA1', 'FileHash-SHA256'):
#
#                            # Whitelisting
#                            if indicator["indicator"] in HASH_WHITELIST:
#                                raise WhiteListedIOC
#
#                            hash = indicator["indicator"]
#                            if self.hash_upper:
#                                hash = indicator["indicator"].upper()
#
#                            self.hash_iocs += "{0}{3}{1} {2}\n".format(
#                                hash,
#                                event["name"].encode('unicode-escape'),
#                                " / ".join(event["references"])[:80],
#                                self.separator)
#
#                        if indicator["type"] == 'FilePath':
#
#                            filename = indicator["indicator"]
#                            if self.filename_regex_out:
#                                filename = my_escape(indicator["indicator"])
#
#                            self.filename_iocs += "{0}{3}{1} {2}\n".format(
#                                filename,
#                                event["name"].encode('unicode-escape'),
#                                " / ".join(event["references"])[:80],
#                                self.separator)

                        if indicator["type"] in ('domain', 'hostname', 'IPv4', 'IPv6', 'CIDR'):
                            indicator = indicator["indicator"]
                            name = event["name"]
                            references = event["references"][0]
                            #print (indicator, name, references)
                            timestamp = datetime.datetime.now(tz)
                            today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
                            db.insert([IOC_OTX(event_date=today, timestamp=timestamp, indicator=indicator, name=name, references=references)])

                    except Exception as e:
                        pass

            except Exception as e:
                traceback.print_exc()

        # Write to files
#        with open(hash_ioc_file, "w") as hash_fh:
#            if self.use_csv_header:
#                hash_fh.write('hash{0}description\n'.format(self.separator))
#            hash_fh.write(self.hash_iocs)
#            print ("{0} hash iocs written to {1}").format(self.hash_iocs.count('\n'), hash_ioc_file)
#        with open(filename_ioc_file, "w") as fn_fh:
#            if self.use_csv_header:
#                fn_fh.write('filename{0}description\n'.format(self.separator))
#            fn_fh.write(self.filename_iocs)
#            print ("{0} filename iocs written to {1}".format(self.filename_iocs.count('\n'), filename_ioc_file))
#        with open(c2_ioc_file, "w") as c2_fh:
#            if self.use_csv_header:
#                c2_fh.write('host{0}description\n'.format(self.separator))
#            c2_fh.write(self.c2_iocs)
#            print ("{0} c2 iocs written to {1}".format(self.c2_iocs.count('\n'), c2_ioc_file))


def my_escape(string):
    return re.sub(r'([\-\(\)\.\[\]\{\}\\\+])',r'\\\1',string)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='OTX IOC Receiver')
    parser.add_argument('-k', help='OTX API key', metavar='APIKEY', default=OTX_KEY)
    # parser.add_argument('-l', help='Time frame in days (default=30)', default=30)
    parser.add_argument('-o', metavar='dir', help='Output directory', default='iocs')
    parser.add_argument('-p', metavar='proxy', help='Proxy server (e.g. http://proxy:8080 or '
                                                    'http://user:pass@proxy:8080', default=None)
    parser.add_argument('--verifycert', action='store_true', help='Verify the server certificate', default=False)
    parser.add_argument('--siem', action='store_true', default=False, help='CSV Output for use in SIEM systems (Splunk)')
    parser.add_argument('--debug', action='store_true', default=False, help='Debug output')

    args = parser.parse_args()

    if len(args.k) != 64:
        print ("Set an API key in script or via -k APIKEY. Go to https://otx.alienvault.com create an account and get your own API key")
        sys.exit(0)

    # Create a receiver
    otx_receiver = OTXReceiver(api_key=args.k, siem_mode=args.siem, debug=args.debug, proxy=args.p)

    # Retrieve the events and store the IOCs
    # otx_receiver.get_iocs_last(int(args.l))
    otx_receiver.get_iocs_last()

    # Write IOC files
    otx_receiver.write_iocs(ioc_folder=args.o)
