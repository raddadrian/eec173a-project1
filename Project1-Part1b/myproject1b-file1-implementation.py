import dpkt
import sys
import datetime
import socket

def parse_pcap(pcap_file):

    f = open(pcap_file, 'rb')
    pcap = dpkt.pcap.Reader(f)
    
    # packet variable to iterate through packets
    pkt = 0 

    # iterate over packets
    for timestamp, data in pcap:

        pkt += 1

        # convert to link layer object
        eth = dpkt.ethernet.Ethernet(data)

        # do not proceed if there is no network layer data
        if not isinstance(eth.data, dpkt.ip6.IP6):
            continue
        
        # extract network layer data
        ip6 = eth.data

        # do not proceed if there is no transport layer data
        # since source and destination IPs are in the IPv6 format
        if not isinstance(ip6.data, dpkt.tcp.TCP):
            continue

        # extract transport layer data
        tcp = ip6.data

        # do not proceed if there is no application layer data
        # here we check length because we don't know protocol yet
        if not len(tcp.data) > 0:
            continue

        # extract application layer data
        # if destination port is 80, it is a http request
        if tcp.dport == 80:
            try:
                print('Secret Detected in Packet: ', pkt)
                print(f'\tTimestamp: {datetime.datetime.utcfromtimestamp(timestamp)}')
                print(f'\tSource IP: {socket.inet_ntop(socket.AF_INET6, ip6.src)} -> Destinaton IP: {socket.inet_ntop(socket.AF_INET6, ip6.dst)}')

                http = dpkt.http.Request(tcp.data)
                # repr() is a method in the dpkt library that outputs packet type, followed by the values of its fields of the HTTP request  
                print('\tHTTP request:', repr(http))
                print('\t -----------------------')

            except:
                pass

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No pcap file specified!")
    else:
        parse_pcap(sys.argv[1])
        