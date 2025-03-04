import os
import socket

def findUsername(text):
    index_from = int(text.find('From:'))
    index_at = int(text.find('@'))
    print(index_from)
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

    c, adress = my_socket.accept()
    print("accepted")
    print(f"Connected to: {adress}")

    while True:
        # Receive data from the client (up to 1024 bytes) and decode it
        data = c.recv(1024).decode()
        print("data received")
        # If no data is received, break the loop
        if not data:
            break
        print(f"Received from client: {data}")
        username = findUsername(data)
        with open(username +"/my_mailbox","a") as myfile:
            myfile.write(data)
    c.close()



if __name__== "__main__":
    main()