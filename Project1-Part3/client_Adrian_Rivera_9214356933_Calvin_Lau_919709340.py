import socket
import json

# specify server host and port to connect to
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5500
jsonData = {
    "server_ip" : "127.0.0.1",
    "server_port" : 7001,
    "message" : "ping"
}


# create a new TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))

    s.send(bytes(json.dumps(jsonData), encoding = 'utf-8'))

    # receive response from server
    data = s.recv(1024)

    # print server response
    print(f"Received {data.decode()!r} from {SERVER_HOST}:{SERVER_PORT}")