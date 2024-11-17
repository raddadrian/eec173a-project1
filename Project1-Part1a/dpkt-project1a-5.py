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

    # variable for FTP count
    ftpCount = 0

    # iterate over packets
    for timestamp, data in pcap:

        pkt += 1

        # convert to link layer object
        eth = dpkt.ethernet.Ethernet(data)

        # do not proceed if there is no network layer data
        if not isinstance(eth.data, dpkt.ip6.IP6) and not  isinstance(eth.data, dpkt.ip.IP):
            continue
        
        # extract network layer data
        ip = eth.data

        # do not proceed if there is no transport layer data
        if not isinstance(ip.data, dpkt.tcp.TCP):
            continue

        # extract transport layer data
        tcp = ip.data

        # do not proceed if there is no application layer data
        if not len(tcp.data) > 0:
            continue

        # if destination port is 21, it is a FTP request
        if tcp.dport == 21:
            try:
                ftpCount += 1
                print(f'Timestamp: {datetime.datetime.utcfromtimestamp(timestamp)}, Source IP: {socket.inet_ntop(socket.AF_INET, ip.src)}, Destination IP: {socket.inet_ntop(socket.AF_INET, ip.dst)}')
            except:
                pass
        elif tcp.sport == 21: # if source port is 21, it is a FTP response
            try:
                ftpCount += 1
                print(f'Timestamp: {datetime.datetime.utcfromtimestamp(timestamp)}, Source IP: {socket.inet_ntop(socket.AF_INET, ip.src)}, Destination IP: {socket.inet_ntop(socket.AF_INET, ip.dst)}')
            except:
                pass
            
    print("FTP Count (port 21): ", ftpCount)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No pcap file specified!")
    else:
        parse_pcap(sys.argv[1])
