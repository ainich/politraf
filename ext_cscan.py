#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Check puplic services on sensys.io and vulners.com

import logging
import json
import yaml
import requests
import time
import datetime
from pytz import timezone

from netaddr import *
import vulners

import dbmodels

# Set logging level
logging.basicConfig(level = logging.INFO)

# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.load(stream))
        CAPI_URL = config['CAPI_URL']
        CUID = config['CUID']
        CSECRET = config['CSECRET']
        SUBNET = config['SUBNET']
        url = config['db_url']
        name = config['username']
        passw = config['password']
        ctimezone = config["time_zone"]
        tz = timezone(ctimezone)
        if len(CUID) != 36:
            print ("Set an API key in /etc/politraf/config.yaml. Go to https://censys.io create an account and get your own API key")
            sys.exit(0)
    except yaml.YAMLError as e:
        logging.error("Error.",e)
    logging.info("Config is OK")

class CENSYSReceiver():

    def __init__(self, url, name, password):
        # Init clickhouse
        try:
            self.db = dbmodels.Database('politraf', db_url=url, username=name, password=passw, readonly=False, autocreate=True)
            self.db.drop_table(dbmodels.OPEN_PORTS)
            self.db.create_table(dbmodels.OPEN_PORTS)
        except Exception as e:
            logging.error("Error.",e)

    def censys_query(self, api_url, api_cuid, api_csecret, subnet):
        logging.info("Starting read from censys ...")
        try:
            ip = IPNetwork(subnet)
            ip_list = list(ip)
            hosts = len(ip_list)
            first_ip = str(ip_list[0])
            last = hosts - 1
            last_ip = str(ip_list[last])
            to_censys = "ip:[" + first_ip + " TO " + last_ip + "]"
            q = {"query": to_censys}
            print (q)
            cresp = requests.post(CAPI_URL+"/search/ipv4", data=json.dumps(q), auth=(CUID, CSECRET), timeout=360)
            if cresp.status_code != 200:
                print (cresp.status_code)
            print ("Read from censys.io complete. Start serach at vulners.com.")
            for hit in cresp.json()["results"]:
                time.sleep(1)
                addr = str(hit["ip"])
                host_info = requests.get(CAPI_URL+"/view/ipv4/"+addr, auth=(CUID, CSECRET), timeout=360)
                os = "None"
                os_v = "None"
                descr = "None"
                service = "None"
                descr = "None"
                product = "None"
                version = "None"
                vdesc = "None"
                title ="None"
                cvelist = "None"
                score = 0
                service = "None"
                if host_info.json().get('metadata'):
                    if host_info.json()["metadata"].get('os'):
                        os = host_info.json()["metadata"]["os"]
                        if host_info.json()["metadata"].get('os_description'):
                            os_v = host_info.json()["metadata"]["os_description"]
                # detect real service
                if host_info.json().get('ports'):
                    for hit in host_info.json()["ports"]:
                        if host_info.json()[hit].get('ssh'):
                            service = "ssh"
                            if host_info.json()[hit]["ssh"]["v2"]["metadata"].get('description'):
                                product = host_info.json()[hit]["ssh"]["v2"]["metadata"]["product"]
                                if host_info.json()[hit]["ssh"]["v2"]["metadata"].get('version'):
                                    version = host_info.json()[hit]["ssh"]["v2"]["metadata"]["version"]
                        if host_info.json()[hit].get('http'):
                            service = "http"
                            if host_info.json()[hit]["http"]["get"]["metadata"].get('description'):
                                product =  host_info.json()[hit]["http"]["get"]["metadata"]["product"]
                                if product == "httpd":
                                    product = "Apache"
                                if product == "nginx":
                                    product = "Nginx"
                                if host_info.json()[hit]["http"]["get"]["metadata"].get('version'):
                                    version =  host_info.json()[hit]["http"]["get"]["metadata"]["version"]
                        if host_info.json()[hit].get('https'):
                            service = "https"
                        if host_info.json()[hit].get('ftp'):
                            service = "ftp"
                            if host_info.json()[hit]["ftp"]["banner"]["metadata"].get('description'):
                                product =  host_info.json()[hit]["ftp"]["banner"]["metadata"]["product"]
                                if host_info.json()[hit]["ftp"]["banner"]["metadata"].get('version'):
                                    version =  host_info.json()[hit]["ftp"]["banner"]["metadata"]["version"]
                        if host_info.json()[hit].get('smb'):
                            service = "smb"
                            if host_info.json()[hit]["smb"]["banner"]["metadata"].get('description'):
                                descr =  host_info.json()[hit]["smb"]["banner"]["metadata"]["description"], host_info.json()[hit]["smb"]["banner"]["smbv1_support"]
                        # use random keys
                        for key in host_info.json()[hit].keys():
                            if service == "None":
                                service = key
                            #print (os, os_v, service, addr, hit, product, version, descr)
                            # get vulners info
                            if product != "None" and version != "None":
                                try:
                                    vulners_api = vulners.Vulners()
                                    results = vulners_api.softwareVulnerabilities(product, version)
                                    #exploit_list = results.get('exploit')
                                    vulnerabilities_list = [results.get(keys) for keys in results if keys not in ['info', 'blog', 'bugbounty']]
                                    vulns = iter(vulnerabilities_list)
                                    for i in vulns:
                                        vulns2 = iter(vulns)
                                        for v in vulns2:
                                            vdesc = v[0]["description"]
                                            title = v[0]["title"]
                                            #cvelist = v[0]["cvelist"]
                                            score = v[0]["cvss"]["score"]
                                            print (os, os_v, service, addr, hit, product, version, descr, score, title)
                                            #print(v)
                                        next(vulns)
                                except:
                                    pass
                            timestamp = datetime.datetime.now(tz)
                            today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
                            self.db.insert([dbmodels.OPEN_PORTS(event_date=today, timestamp=timestamp, os = os, os_v = os_v, srv = service, addr = addr, port = hit, product = product, version = version, descr = descr, vdesc = vdesc, title = title, cvelist = cvelist, score = score)])

            return cresp
        except Exception as e:
            logging.error("Error.",e)
        logging.info("Read from censys and vulners complete")


def main():

    # Create a receiver
    censys_receiver = CENSYSReceiver(url=url, name=name, password=passw)

    # Retrieve the info about network
    censys_receiver.censys_query(api_url=CAPI_URL, api_cuid=CUID, api_csecret=CSECRET, subnet=SUBNET)


if __name__ == '__main__':
    main()





