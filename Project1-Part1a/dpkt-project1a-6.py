import socket
import datetime
import dpkt
import sys

def parse_pcap(pcap_file):

    # read the pcap file
    f = open(pcap_file, 'rb')
    pcap = dpkt.pcap.Reader(f)
    port_numbers = {}
    # iterate over packets
    for timestamp, data in pcap:

        # convert to link layer object
        eth = dpkt.ethernet.Ethernet(data)
        #print(eth)

        # do not proceed if there is no network layer data
        if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
            continue
        
        # extract network layer data
        ip = eth.data
        if len(ip.dst) == 4:
            dst_ip = socket.inet_ntoa(ip.dst)
        else:
            continue
        
        # do not proceed if there is no transport layer data
        if not isinstance(ip.data, dpkt.udp.UDP):
            continue

        # extract transport layer data
        udp = ip.data

        # do not proceed if there is no application layer data
        # here we check length because we don't know protocol yet
        if not len(udp.data) > 0:
            continue

        # extract application layer data

        port = udp.dport
        if port in port_numbers:
            port_numbers[port] += 1
        else:
            port_numbers[port] = 1

        ## if destination port is 4500, it is a ssh request
        if udp.dport == 4500:
            try:
                print(f'Timestamp: {datetime.datetime.utcfromtimestamp(timestamp)}, Destination IP: {dst_ip}, Port Number: {udp.dport}')  
            except:
                pass
                
        ## if source port is 4500, it is a ssh response
        elif udp.sport == 4500:
            try:
                print(f'Timestamp: {datetime.datetime.utcfromtimestamp(timestamp)}, Destination IP: {dst_ip}, Port Number: {udp.dport}')
            except:
                pass      
 

    for port, count in port_numbers.items():
        print(f"Port: {port}, Count: {count}")
    


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No pcap file specified!")
    else:
        parse_pcap(sys.argv[1])