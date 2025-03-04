import socket

client_port = 12345
client_socket = socket.socket()
hostname = socket.gethostname()
client_socket.connect((hostname,client_port))

while True:

    str = input('S : ')
    client_socket.send(str.encode())
    received_text =client_socket.recv(1024).decode()
    print(f"N: {received_text}")
    if str == "Exit" or received_text=="ERROR":
        break

client_socket.close()