import dpkt
import sys
import socket
import datetime

def parse_pcap(pcap_file):
    # Open the pcap file using a context manager
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        # Iterate over packets
        pkt = 0
        for timestamp, data in pcap:
            pkt += 1

            try:
                # Convert to link layer object
                eth = dpkt.ethernet.Ethernet(data)

                # Check if it contains an IP packet
                if not isinstance(eth.data, dpkt.ip.IP):
                    continue

                # Extract IP layer data
                ip = eth.data

                # Check if it's an ICMP packet
                if isinstance(ip.data, dpkt.icmp.ICMP):
                    icmp = ip.data

                    # Extract and format source and destination IPs
                    src_ip = socket.inet_ntop(socket.AF_INET, ip.src)
                    dst_ip = socket.inet_ntop(socket.AF_INET, ip.dst)

                    # Print packet information
                    print(f'Packet #{pkt}')
                    print(f'\tTimestamp: {datetime.datetime.utcfromtimestamp(timestamp)}')
                    print(f'\tSource IP: {src_ip} -> Destination IP: {dst_ip}')
                    
                    # Print ICMP properties
                    print('\t********* ICMP Packet Properties *********')
                    print(f'\tTTL: {ip.ttl} Type: {icmp.type} Code: {icmp.code}\n')

            except dpkt.UnpackError:
                print(f'Packet #{pkt} could not be unpacked and was skipped.')
            except (socket.error, ValueError) as e:
                print(f'Packet #{pkt} encountered an IP formatting error: {e}')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py <pcap_file_1> <pcap_file_2>")
    else:
        print('*************** Printout for ass1_2.pcap: ***************\n')
        parse_pcap(sys.argv[1])
        print('*************** Printout for ass1_3.pcap: ***************\n')
        parse_pcap(sys.argv[2])
