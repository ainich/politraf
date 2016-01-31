import pyshark

cap = pyshark.LiveCapture(interface='eth0', bpf_filter='ip')


def print_conversation_header(pkt):
    try:
        # UDP traf
        protocol = pkt.transport_layer
        src_addr = pkt.ip.src
        src_port = pkt[pkt.transport_layer].srcport
        dst_addr = pkt.ip.dst
        dst_port = pkt[pkt.transport_layer].dstport
        print '%s  %s:%s --> %s:%s' % (protocol, src_addr, src_port, dst_addr, dst_port)
        http_referer = "0"
        http_host = "0"
        # TCP traf
        if protocol == "TCP":
            http = pkt.http.request
            if http == "1":
                http_referer = pkt.http.referer
                http_host = pkt.http.host
        print '%s  %s:%s %s %s --> %s:%s' % (protocol, src_addr, src_port, http_referer, http_host, dst_addr, dst_port)

    except AttributeError as e:
        # ignore packets that aren't TCP/UDP or IPv4
        pass
 
cap.apply_on_packets(print_conversation_header)
