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
        logging.error("Error.", e)
    logging.info("Config is OK")


class CENSYSReceiver():

    def __init__(self, url, name, password):
        # Init clickhouse
        try:
            self.db = dbmodels.Database('politraf', db_url=url, username=name, password=passw, readonly=False, autocreate=True)
            self.db.drop_table(dbmodels.OPEN_PORTS)
            self.db.create_table(dbmodels.OPEN_PORTS)
        except Exception as e:
            logging.error("Error.", e)

    def censys_query_net(self, api_url, api_cuid, api_csecret, subnet):
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
            logging.info(q)
            self.cresp = requests.post(CAPI_URL+"/search/ipv4", data=json.dumps(q), auth=(CUID, CSECRET), timeout=360)
            if self.cresp.status_code != 200:
                logging.error(self.cresp.status_code)
            logging.info("Read hosts list from censys.io complete ...")
        except Exception as e:
            logging.error("Error.", e)

    def censys_query_host(self, api_url, api_cuid, api_csecret):
        try:
            for hit in self.cresp.json()["results"]:
                time.sleep(1)
                self.addr = str(hit["ip"])
                self.host_info = requests.get(CAPI_URL+"/view/ipv4/"+self.addr, auth=(CUID, CSECRET), timeout=360)
                if self.host_info.status_code != 200:
                    logging.error(self.host_info.status_code)
                self.vulners_query()
        except Exception as e:
            logging.error("Error.", e)

    def vulners_query(self):
        try:
            os = "None"
            os_v = "None"
            descr = "None"
            service = "None"
            descr = "None"
            product = "None"
            version = "None"
            vdesc = "None"
            title = "None"
            cvelist = "None"
            score = 0
            service = "None"
            if self.host_info.json().get('metadata'):
                if self.host_info.json()["metadata"].get('os'):
                    os = self.host_info.json()["metadata"]["os"]
                    if self.host_info.json()["metadata"].get('os_description'):
                        os_v = self.host_info.json()["metadata"]["os_description"]
            # detect real service
            if self.host_info.json().get('ports'):
                for hit in self.host_info.json()["ports"]:
                    if self.host_info.json()[hit].get('ssh'):
                        service = "ssh"
                        if self.host_info.json()[hit]["ssh"]["v2"]["metadata"].get('description'):
                            product = self.host_info.json()[hit]["ssh"]["v2"]["metadata"]["product"]
                            if self.host_info.json()[hit]["ssh"]["v2"]["metadata"].get('version'):
                                version = self.host_info.json()[hit]["ssh"]["v2"]["metadata"]["version"]
                    if self.host_info.json()[hit].get('http'):
                        service = "http"
                        if self.host_info.json()[hit]["http"]["get"]["metadata"].get('description'):
                            product = self.host_info.json()[hit]["http"]["get"]["metadata"]["product"]
                            if product == "httpd":
                                product = "Apache"
                            if self.host_info.json()[hit]["http"]["get"]["metadata"].get('version'):
                                version = self.host_info.json()[hit]["http"]["get"]["metadata"]["version"]
                    if self.host_info.json()[hit].get('https'):
                        service = "https"
                    if self.host_info.json()[hit].get('ftp'):
                        service = "ftp"
                        if self.host_info.json()[hit]["ftp"]["banner"]["metadata"].get('description'):
                            product = self.host_info.json()[hit]["ftp"]["banner"]["metadata"]["product"]
                            if self.host_info.json()[hit]["ftp"]["banner"]["metadata"].get('version'):
                                version = self.host_info.json()[hit]["ftp"]["banner"]["metadata"]["version"]
                    if self.host_info.json()[hit].get('smb'):
                        service = "smb"
                        if self.host_info.json()[hit]["smb"]["banner"]["metadata"].get('description'):
                            descr = (self.host_info.json()[hit]["smb"]["banner"]["metadata"]["description"], self.host_info.json()[hit]["smb"]["banner"]["smbv1_support"])
                    # use random keys
                    for key in self.host_info.json()[hit].keys():
                        if service == "None":
                            service = key
                        # get vulners info
                        if product != "None" and version != "None":
                            vulners_api = vulners.Vulners()
                            try:
                                results = vulners_api.softwareVulnerabilities(product, version)
                                vulnerabilities_list = [results.get(keys) for keys in results if keys not in ['info', 'blog', 'bugbounty']]
                                vulns = iter(vulnerabilities_list)
                                for i in vulns:
                                    vulns2 = iter(vulns)
                                    for v in vulns2:
                                        vdesc = v[0]["description"]
                                        title = v[0]["title"]
                                        score = v[0]["cvss"]["score"]
                            except:
                                pass
                        log = (os, os_v, service, self.addr, hit, product, version, descr, score, title)
                        logging.info(log)
                self.os = os
                self.os_v = os_v
                self.descr = descr
                self.service = service
                self.descr = descr
                self.product = product
                self.version = version
                self.vdesc = vdesc
                self.title = title
                self.cvelist = cvelist
                self.score = score
                self.service = service
                self.hit = hit

                self.write_to_clickhouse()

        except Exception as e:
            logging.error("Error.", e)

    def write_to_clickhouse(self):
        try:
            timestamp = datetime.datetime.now(tz)
            today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
            self.db.insert([dbmodels.OPEN_PORTS(event_date=today, timestamp=timestamp, os=self.os,
                          os_v = self.os_v, srv = self.service, addr = self.addr, port = self.hit,
                          product = self.product, version = self.version, descr = self.descr,
                          vdesc = self.vdesc, title = self.title, cvelist = self.cvelist, score = self.score)])
        except Exception as e:
            logging.error("Error.", e)


def main():

    # Create a receiver
    censys_receiver = CENSYSReceiver(url=url, name=name, password=passw)

    # Retrieve the info about network
    censys_receiver.censys_query_net(api_url=CAPI_URL, api_cuid=CUID, api_csecret=CSECRET, subnet=SUBNET)
    censys_receiver.censys_query_host(api_url=CAPI_URL, api_cuid=CUID, api_csecret=CSECRET)

    logging.info("Read from censys and vulners complete")


if __name__ == '__main__':
    main()
