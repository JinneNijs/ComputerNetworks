import socket

client_port = int(input('give client_port '))
client_socket = socket.socket()
hostname = socket.gethostname()
client_socket.connect((hostname,client_port))

while True:
    str = input('S : ')
    client_socket.send(str.encode())
    print(f"N: {client_socket.recv(1024).decode()}")
    if str == "Exit":
        break
client_socket.close()