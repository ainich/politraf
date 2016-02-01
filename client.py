#!/usr/bin/python
# -*- coding: utf-8
import pyshark
import os
import glob

cap = pyshark.LiveCapture(interface='enp3s0f1', bpf_filter='src net 172 and (tcp dst port 80 or tcp dst port 8080 or tcp dst port 443 or udp port 53)')
# Define tmp pcap
tmpfiles = glob.glob('/tmp/wireshark*')

def print_conversation_header(pkt):
    try:
        protocol = pkt.transport_layer
        src_addr = pkt.ip.src
        src_port = pkt[pkt.transport_layer].srcport
        dst_addr = pkt.ip.dst
        dst_port = pkt[pkt.transport_layer].dstport
# UDP traf
        if protocol == "UDP":
            print '%s  %s:%s --> %s:%s' % (protocol, src_addr, src_port, dst_addr, dst_port)
# DNS request
            if pkt.dns.qry_name:
                print 'DNS Request from %s: %s' % (pkt.ip.src, pkt.dns.qry_name)
            elif pkt.dns.resp_name:
                print 'DNS Response from %s: %s' % (pkt.ip.src, pkt.dns.resp_name)
# TCP traf
        if protocol == "TCP":
#            http_referer = "0"
#            http_host = "0"
#            http = "0"
#            http = pkt.http.request
#            if pkt.http.request:
            http_referer = pkt.http.referer
            http_host = pkt.http.host
            print '%s  %s:%s %s %s --> %s:%s' % (protocol, src_addr, src_port, http_referer, http_host, dst_addr, dst_port)
#            print '%s  %s:%s --> %s:%s' % (protocol, src_addr, src_port, dst_addr, dst_port)

    except AttributeError as e:
        #i gnore packets that aren't TCP/UDP or IPv4
        pass

x = 1
while True:
    for f in tmpfiles:
        os.remove(f)
    cap.apply_on_packets(print_conversation_header, timeout=20)
    x += 1