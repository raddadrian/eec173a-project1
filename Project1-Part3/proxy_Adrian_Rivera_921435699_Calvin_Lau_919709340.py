import socket
import json

PROXY_IP = '127.0.0.1'
PROXY_PORT = 5500
IP_Blocklist = []

def handle_client(client_socket, client_addr):
    #Receive JSON
    data = client_socket.recv(1024)
    if not data:
        return
    
    #Open and Read JSON
    try:
        jsonData = data.decode(('utf-8'))
        dstData = json.loads(jsonData)
        DST_IP = dstData["server_ip"]
        DST_PORT = dstData["server_port"]
        MSG = dstData["message"]
    except:
        return

    #Check blocklist
    if DST_IP in IP_Blocklist:
        client_socket.sendall("Error: IP in Blocklist".encode())

    #If not on blocklist, send MSG to DST server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_out:
        proxy_out.connect((DST_IP, DST_PORT))

        proxy_out.sendall(MSG.encode('utf-8'))

        response = proxy_out.recv(1024)

        if response:
            client_socket.sendall(response)
        else:
            client_socket.sendall("No response".encode())


    client_socket.close()


def main():
    #Create listening TCP socket
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
        # Allow port reuse
        proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            proxy_socket.bind((PROXY_IP, PROXY_PORT))
            #Listen for requests
            proxy_socket.listen()
            #Accept Client
            while True:
                client_socket, client_addr = proxy_socket.accept()
                print(f"Accepted connection from {client_addr}")
                handle_client(client_socket, client_addr)
                
        except KeyboardInterrupt:
            print("\nShutting down proxy...")
        except Exception as e:
            print(f"Error in main loop: {str(e)}")

if __name__ == "__main__":
    main()