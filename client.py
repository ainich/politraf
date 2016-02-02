#!/usr/bin/python
# -*- coding: utf-8
import pyshark
import os
import glob

cap = pyshark.LiveCapture(interface='eth0', bpf_filter='src net 192.168.1 and (tcp dst portrange 1-1024 or udp dst port 53)')
# Define tmp pcap
tmpfiles = glob.glob('/tmp/wireshark*')


def print_conversation_header(pkt):
    protocol = pkt.transport_layer
    src_addr = pkt.ip.src
    src_port = pkt[pkt.transport_layer].srcport
    dst_addr = pkt.ip.dst
    dst_port = pkt[pkt.transport_layer].dstport
    #sslcheck = "SSL"
    #httpcheck = "HTTP"

    # UDP traf
    if protocol == "UDP":
        print '%s  %s:%s --> %s:%s' % (protocol, src_addr, src_port, dst_addr, dst_port)
        # DNS request
        if pkt.dns.qry_name:
            print 'DNS Request from %s: %s' % (pkt.ip.src, pkt.dns.qry_name)
        elif pkt.dns.resp_name:
            print 'DNS Response from %s: %s' % (pkt.ip.src, pkt.dns.resp_name)
    else:
        if "SSL" in pkt:
            print 'SSL %s  %s:%s --> %s:%s' % (protocol, src_addr, src_port, dst_addr, dst_port)

        elif "HTTP" in pkt:
            http_host = pkt.http.host
            print 'HTTP %s  %s:%s %s --> %s:%s' % (protocol, src_addr, src_port, http_host, dst_addr, dst_port)

        else:
            print '%s  %s:%s --> %s:%s' % (protocol, src_addr, src_port, dst_addr, dst_port)


while True:
    i = 0
    while i < 1024:
        cap.apply_on_packets(print_conversation_header)
        i += 1
    os.remove(tmpfiles)