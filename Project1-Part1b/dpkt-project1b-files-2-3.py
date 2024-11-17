import dpkt
import sys
import socket
import datetime

def parse_pcap(pcap_file):

    # read the pcap file
    f = open(pcap_file, 'rb')
    pcap = dpkt.pcap.Reader(f)

    # iterate over packets
    pkt = 0

    for timestamp, data in pcap:
        pkt += 1

        # convert to link layer object
        eth = dpkt.ethernet.Ethernet(data)

        # do not proceed if there is no network layer data
        if not isinstance(eth.data, dpkt.ip.IP):
            continue
        
        # extract network layer data
        ip = eth.data

        # extracting the Time-to-Live (TTL) to inspect how many hops the packets went through
        # which can help us analyze further if a VPN or proxy was used
        # a TTL of 1 or 2 might indicate traffic passing through a VPN or proxy o.t.w, a TTL of either 64 or 128 might indicate communication w/out a proxy or VPN
        TTL = ip.ttl

        # since source and destination IPs are in the IPv4 format
        # the protocol of the packets in the ass1_2.pcap and ass1_3.pcap files are ICMP, therfore there is no assigned port number
        if isinstance(ip.data, dpkt.icmp.ICMP):
            icmp = ip.data

            print('Packet #', pkt,)
            print(f'\tTimestamp: {datetime.datetime.utcfromtimestamp(timestamp)}')
            print(f'\tSource IP: {socket.inet_ntop(socket.AF_INET, ip.src)} -> Destinaton IP: {socket.inet_ntop(socket.AF_INET, ip.dst)}\n')

            # printing the TTL gives us information if a vpn or proxy was used
            # printing the Type gives us information about which type of messages the ICMP packets are
            # printing the Code gives us information about the messages' purpose 
            print('\t********* ICMP Packet Properties *********')
            print('\tTTL:%d Type:%d Code:%d\n' % (TTL, icmp.type, icmp.code))
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No pcap file specified!")
    else:
        print('*************** Printout for ass1_2.pcap: ***************\n')
        parse_pcap(sys.argv[1])
        print('*************** Printout for ass1_3.pcap: ***************\n')
        parse_pcap(sys.argv[2])