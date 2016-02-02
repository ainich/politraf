#!/usr/bin/python
# -*- coding: utf-8
import pyshark
import os
import glob
import requests
import json


# PyShark config
cap = pyshark.LiveCapture(interface='eth0', bpf_filter='src net 192.168.1 and (tcp dst portrange 1-1024 or udp dst port 53)')


def print_conversation_header(pkt):
    protocol = pkt.transport_layer
    src_addr = pkt.ip.src
    src_port = pkt[pkt.transport_layer].srcport
    dst_addr = pkt.ip.dst
    dst_port = pkt[pkt.transport_layer].dstport

    # UDP traf
    if protocol == "UDP":
        #msg = '%s %s %s %s %s' % (protocol, src_addr, src_port, dst_addr, dst_port)
        #print msg
        # DNS request
        if pkt.dns.qry_name:
            msg = '%s %s %s %s %s %s' % (protocol, src_addr, src_port, dst_addr, dst_port, pkt.dns.qry_name)
            print msg
        elif pkt.dns.resp_name:
            msg = '%s %s %s %s %s %s' % (protocol, src_addr, src_port, dst_addr, dst_port, pkt.dns.resp_name)
            print msg
    # TCP traf
    else:
        if "SSL" in pkt:
            msg = '%s %s %s %s %s %s' % (protocol, src_addr, src_port, dst_addr, dst_port, "none")
            print msg
        elif "HTTP" in pkt:
            http_host = pkt.http.host
            msg = '%s %s %s %s %s %s' % (protocol, src_addr, src_port, dst_addr, dst_port, http_host)
            print msg
        else:
            msg = '%s %s %s %s %s %s' % (protocol, src_addr, src_port, dst_addr, dst_port, "none")
            print msg
    requests.post("http://10.1.1.222:5002", data=msg, timeout=160)

while True:
    # Define tmp pcap
    tmpfiles = glob.glob('/tmp/wireshark*')
    for f in tmpfiles:
        os.remove(f)
    try:
        cap.apply_on_packets(print_conversation_header, timeout=180)
    except Exception as e:
        pass
