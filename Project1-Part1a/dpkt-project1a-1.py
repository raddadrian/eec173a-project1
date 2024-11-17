import socket
import datetime
import dpkt
import sys

def parse_pcap(pcap_file):

    # read the pcap file
    f = open(pcap_file, 'rb')
    pcap = dpkt.pcap.Reader(f)

    # variable to iterate over packets
    pkt = 0

    # icmp variable to count the pings to Google
    icmp_count = 0 

    # iterate over packets
    for timestamp, data in pcap:

        pkt += 1

        # convert to link layer object
        eth = dpkt.ethernet.Ethernet(data)

        # do not proceed if there is no network layer data
        if not isinstance(eth.data, dpkt.ip.IP):
            continue
        
        # extract network layer data
        ip = eth.data
        
        # do not proceed if there is no network layer data
        if not isinstance(eth.data, dpkt.ip.IP):
            continue

        # extract network layer data
        ip = eth.data

        # When you ping Google, you won't see any port numbers because 
        # ping does not use TCP or UDP, but uses ICMP
        if isinstance(ip.data, dpkt.icmp.ICMP):
            icmp = ip.data

            # To track only the 20 ping requests and not the reciprocated 20 responses from Google
            # Type 8 indicates a ping request
            if icmp.type == 8:
                icmp_count += 1

                print("Ping to Google detected")
                print(f'Timestamp: {datetime.datetime.utcfromtimestamp(timestamp)}, Source IP: {socket.inet_ntop(socket.AF_INET, ip.src)}, Destination IP: {socket.inet_ntop(socket.AF_INET, ip.dst)}')

    print(f'Total ping packets to Google : {icmp_count}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No pcap file specified!")
    else:
        parse_pcap(sys.argv[1])