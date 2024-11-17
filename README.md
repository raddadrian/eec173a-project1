# eec173a-project1
EEC 173A - Computer Networks Project 1

This project is for EEC 173A.

Part 1: PCAP Analysis
The first part of the project has two subparts:
  Part A: Monitoring Live Network Traffic
    -We performed certain network activities while running Wireshark in the background.
      -The activities:
        -Ping google.com for 20 packets
        -Visiti https://example.com 
        -Visit https://httpforever.com
        -Visit https://www.tmz.com
        -Access an FTP server
        -SSH into a CSIF machine 
        
  Part B: Analyzing Network Traffic in a pcap File
    -We were given 3 pcap files generated using Wireshark listening over wireless. 
      -The first pacap captures multiple requests some of which send secret sensitive information from a client to a server
      -We analyze the pcap files and list all secrets that were sent to the server
      -Our program output each secret in a separate line
      -The second and third pcap files capture traffic from a very specific activity with a subtle difference
        -For these pcap files, we wrote a program to figure out the actovoty performed in the pcap files and identify what was different when performing the activity across the two pcap files

Part 2: Implementing iPerf
  In this part, we built a UDP server and client (both hosted on localhost) using the socket API in Python.
    -We send 100 megabytes of data from the client to the server.
    -The server should measure the throughput (amount of data received / time taken to receive them) and send it back to the client.
    -The client prints the throughput value received from the server.
    -The calculated throughput is computed in kilobytes per second.

Part 3: Proxy Server
  -In this part, we implemented ping-pong servers using TCP Sockets, but instead of having the client talk to the server directly, we implemented a proxy server that forwards requests from the client to the server.
  -The proxy server extracts the server's IPfrom the message and forwards the message to the server.
    -Once the server responds, the proxy forwards the message back to the client.
  -The proxy also implements an IP blocklist consisiting pf several IP addresses.
    -Whenever it finds that the server IP is in the blocklist, it does not forward the request and replies with an "Error" message instead.

