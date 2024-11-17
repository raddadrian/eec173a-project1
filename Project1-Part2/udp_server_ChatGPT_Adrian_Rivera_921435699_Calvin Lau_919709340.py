import socket
import time

# Set up server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 12345))
print("Server is ready to receive data")

# Configuration
data_size_bytes = 100 * 1024 * 1024  # 100 MB in bytes
received_data = b''
start_time = time.time()

# Receiving data
while len(received_data) < data_size_bytes:
    data, addr = server_socket.recvfrom(4096)
    received_data += data

end_time = time.time()
elapsed_time = end_time - start_time  # Time taken to receive data in seconds

# Calculate throughput
throughput_kbps = (len(received_data) / 1024) / elapsed_time  # in kilobytes per second

# Send throughput back to client
server_socket.sendto(str(throughput_kbps).encode(), addr)
print(f"Throughput sent to client: {throughput_kbps:.2f} KBps")

# Close server socket
server_socket.close()
