import os
import socket

def findUsername(text):
    index_from = int(text.find('From:'))
    index_at = int(text.find('@'))
    if index_from ==-1:
        return 0
    Username = text[index_from+5:index_at]
    return Username


def main():
    #specify which port to listen on
    my_port = int(input("Specify my_port "))
    #get the hostname of the server
    hostname = socket.gethostname()
    print(hostname)

    #create a socket
    my_socket = socket.socket()

    #bind the socket to the host and port
    my_socket.bind((hostname,my_port))
    print("binded")
    #wait for a connection, specify number of simultaneous clients
    my_socket.listen(1)
    print("done listening")
    #adress = IP-adress/host,port
    #Accept a connection.
    # The socket must be bound to an address and listening for connections.
    # The return value is a pair (conn, address) where conn is a new socket object
    # usable to send and receive data on the connection,
    # and address is the address bound to the socket on the other end of the connection.
    c, adress = my_socket.accept()
    print("accepted")
    print(f"Connected to: {adress}")

    while True:
        # Receive data from the client (up to 1024 bytes) and decode it
        data = c.recv(1024).decode()
        print("data received")
        # If no data is received, break the loop
        if not data or data == "Exit":
            break
        print(f"Received from client: {data}")
        username = findUsername(data)
        if username == 0:
            str = input("S: ")
            c.send(str.encode())
        else:
            with open(username +"/my_mailbox","a") as myfile:
                myfile.write(data)
    c.close()



if __name__== "__main__":
    main()