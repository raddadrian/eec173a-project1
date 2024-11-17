import socket
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5500

HOST = '127.0.0.1'
PORT = 5501

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    client_socket.bind((HOST, PORT))
    total_packet_size = 100 * (2 ** 20) #100 mb in bytes
    packet_size = 4 * (2 ** 10) #8kb
    packet_number = total_packet_size // packet_size #total number of bytes / packet_size
    data = b'a' * packet_size

    print("Sending 100MB to server")
    for x in range(packet_number):
        client_socket.sendto(data, (SERVER_HOST, SERVER_PORT))
        time.sleep(0.000001)
        
    client_socket.sendto(b'END', (SERVER_HOST, SERVER_PORT))

    bytes_received = float(client_socket.recv(packet_size))
    print(f"Total Bytes Received: {bytes_received} MB")

    duration = float(client_socket.recv(packet_size))
    print(f"Duration: {duration:.2f} seconds")

    throughput = float(client_socket.recv(packet_size))
    print(f"Throughput: {throughput:.2f} kBps")

    client_socket.close()

