import socket
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5500

HOST = '127.0.0.1'
PORT = 5501

# Define constants for packet size and total data size
TOTAL_PACKET_SIZE = 100 * (2 ** 20)  # 100 MB in bytes
PACKET_SIZE = 4 * (2 ** 10)  # 4 KB
PACKET_NUMBER = TOTAL_PACKET_SIZE // PACKET_SIZE  # Total number of packets to send
DATA = b'a' * PACKET_SIZE

try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.bind((HOST, PORT))  # Bind the socket to the local host and port
        print("Sending 100MB to server")

        for x in range(PACKET_NUMBER):
            client_socket.sendto(DATA, (SERVER_HOST, SERVER_PORT))
            # Optional: Sleep is removed unless absolutely necessary
            # time.sleep(0.000001)

        # Send the end signal to the server
        client_socket.sendto(b'END', (SERVER_HOST, SERVER_PORT))

        # Receiving data (total bytes, duration, and throughput)
        bytes_received = float(client_socket.recv(PACKET_SIZE))
        print(f"Total Bytes Received: {bytes_received / (2**20):.2f} MB")

        duration = float(client_socket.recv(PACKET_SIZE))
        print(f"Duration: {duration:.2f} seconds")

        throughput = float(client_socket.recv(PACKET_SIZE))
        print(f"Throughput: {throughput / 1024:.2f} kBps")

except socket.error as e:
    print(f"Socket error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
