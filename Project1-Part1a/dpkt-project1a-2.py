import socket
import datetime
import dpkt
import sys

def parse_pcap(pcap_file):
    # IP address to filter for example.com
    EXAMPLE_COM_IP = "93.184.215.14"

    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        # iterate over packets
        httpCounts = 0
        httpsCounts = 0

        for timestamp, data in pcap:
            # convert to link layer object
            eth = dpkt.ethernet.Ethernet(data)
            #print(eth)

            # do not proceed if there is no network layer data
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                src_IP = socket.inet_ntop(socket.AF_INET, ip.src)
                dst_IP = socket.inet_ntop(socket.AF_INET, ip.dst)

                if src_IP != EXAMPLE_COM_IP and dst_IP != EXAMPLE_COM_IP:
                    continue

            else:
                continue
            
            # extract network layer data
            # ip = eth.data

            # do not proceed if there is no transport layer data
            if not isinstance(ip.data, dpkt.tcp.TCP):
                continue

            # extract transport layer data
            tcp = ip.data

            # here we check length because we don't know protocol yet
            if not len(tcp.data) > 0:
                continue

            # if destination port is 80, it is a http request
            if tcp.dport == 80 or tcp.sport == 80: 
                httpCounts += 1
                print(f'Timestamp: {datetime.datetime.utcfromtimestamp(timestamp)}, Source IP: {src_IP}, Destination IP: {dst_IP}')
            elif tcp.dport == 443 or tcp.sport == 443: # checking if there are any HTTPS packets. if desination port is 443, it is a https request
                httpsCounts += 1
                print(f'Timestamp: {datetime.datetime.utcfromtimestamp(timestamp)}, Source IP: {src_IP}, Destination IP: {dst_IP}')


    print('HTTP Count (Port 80): ', httpCounts)
    print('HTTPS Count (Port 443): ', httpsCounts)
            

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No pcap file specified!")
    else:
        parse_pcap(sys.argv[1])