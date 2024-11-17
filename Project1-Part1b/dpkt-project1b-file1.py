import socket
import datetime
import dpkt
import sys

def parse_pcap(pcap_file):

    # read the pcap file
    f = open(pcap_file, 'rb')
    pcap = dpkt.pcap.Reader(f)
    
    tcp_ports = {}
    udp_ports = {}

    # iterate over packets
    for timestamp, data in pcap:

        # convert to link layer object
        eth = dpkt.ethernet.Ethernet(data)

        # do not proceed if there is no network layer data
        if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
            continue
        
        # extract network layer data
        ip = eth.data

        # extract transport layer data
        if isinstance(ip.data, dpkt.tcp.TCP):
            tcp = ip.data
            if not len(tcp.data) > 0:
                continue
            
            sport, dport = tcp.sport, tcp.dport

            if sport in tcp_ports:
                tcp_ports[sport] += 1
            else:
                tcp_ports[sport] = 1
            if dport in tcp_ports:
                tcp_ports[dport] += 1
            else:
                tcp_ports[dport] = 1

            ## if destination port is 80, it is a http request
            if dport == 80:
                try:
                    http = dpkt.http.Request(tcp.data)
                    print(http)
                except:
                    pass
                
            ## if source port is 80, it is a http response
            elif sport == 80:
                try:
                    http = dpkt.http.Response(tcp.data)
                    print(http)
                except:
                    pass
            

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No pcap file specified!")
    else:
        parse_pcap(sys.argv[1])