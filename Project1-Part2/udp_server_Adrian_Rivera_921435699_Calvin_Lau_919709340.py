import socket
import time

HOST = '127.0.0.1'
PORT = 5500
BUFFER_SIZE = 200 * (2 ** 20)  # 200 MB buffer
BYTES_RECEIVED = 0
START_TIME = 0
END_TIME = 0
RETURN_ADDRESS = None

def send_response(data, address):
    """Helper function to send data to the client."""
    server_socket.sendto(data, address)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")

    server_socket.settimeout(10)  # Timeout after 10 seconds
    START_TIME = time.time()

    while True:
        try:
            print("Waiting for data...")
            data, addr = server_socket.recvfrom(BUFFER_SIZE)

            # Check for the 'END' signal to terminate the loop
            if data == b'END':
                print("Received end signal, breaking out of loop.")
                break

            END_TIME = time.time()
            RETURN_ADDRESS = addr

            print(f"Received {len(data)} bytes from {addr} at time {END_TIME}")
            BYTES_RECEIVED += len(data)
            print(f"Total bytes received: {BYTES_RECEIVED}")

        except socket.timeout:
            print("Timeout reached, breaking out of loop.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # Calculate metrics
    duration = END_TIME - START_TIME
    throughput = (BYTES_RECEIVED / duration) / (2 ** 10)  # kBps
    MB_RECEIVED = BYTES_RECEIVED / (2 ** 20)  # MB

    print(f"Duration: {duration:.2f} seconds")
    print(f"Throughput: {throughput:.2f} kBps")
    print(f"Total Bytes Received: {MB_RECEIVED:.2f} MB")

    # Send the results back to the client
    send_response(bytes(f"{MB_RECEIVED:.2f}", 'utf-8'), RETURN_ADDRESS)
    send_response(bytes(f"{duration:.2f}", 'utf-8'), RETURN_ADDRESS)
    send_response(bytes(f"{throughput:.2f}", 'utf-8'), RETURN_ADDRESS)
