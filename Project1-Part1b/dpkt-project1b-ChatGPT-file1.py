import socket
import datetime
import dpkt
import sys

def parse_pcap(pcap_file):
    # read the pcap file
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        
        tcp_ports = {}
        udp_ports = {}

        # iterate over packets
        for timestamp, data in pcap:
            # convert to link layer object
            eth = dpkt.ethernet.Ethernet(data)

            # check if there is network layer data
            if not isinstance(eth.data, (dpkt.ip.IP, dpkt.ip6.IP6)):
                continue
            
            # extract network layer data
            ip = eth.data

            # extract transport layer data
            if isinstance(ip.data, dpkt.tcp.TCP):
                tcp = ip.data
                if len(tcp.data) == 0:
                    continue

                sport, dport = tcp.sport, tcp.dport
                tcp_ports[sport] = tcp_ports.get(sport, 0) + 1
                tcp_ports[dport] = tcp_ports.get(dport, 0) + 1

                # Print HTTP data if port 80 (HTTP traffic)
                if dport == 80:
                    try:
                        http = dpkt.http.Request(tcp.data)
                        print(f"HTTP Request at {datetime.datetime.fromtimestamp(timestamp)}: {http}")
                    except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                        pass
                    
                elif sport == 80:
                    try:
                        http = dpkt.http.Response(tcp.data)
                        print(f"HTTP Response at {datetime.datetime.fromtimestamp(timestamp)}: {http}")
                    except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                        pass

    # Print summarized port usage
    print("\nTCP Ports Usage:", tcp_ports)
    print("UDP Ports Usage:", udp_ports)

def main():
    if len(sys.argv) < 2:
        print("No pcap file specified! Usage: python script.py <pcap_file>")
        sys.exit(1)
    
    parse_pcap(sys.argv[1])

if __name__ == '__main__':
    main()
