import socket
from fileinput import close
import pickle


def mailSearchingServer(socket, option):
    return


def checkTextFile(user, password):
    with open("userinfo.txt") as file:
        # read all lines of the file
        lines = file.readlines()
        for line in lines:
            # if line starts with space, end of file
            if line.startswith(" "):
                break
            # separate user from password
            username = line.split()[0]
            if user == username:
                actual_password = line.split()[1]
                if password == actual_password:
                    file.close()
                    return 1
    file.close()
    return 0


def userAuthentication(socket):
    while True:
        user_text = "USER: "
        socket.send(user_text.encode())
        received_user = socket.recv(1024).decode()
        password_test = "PASS: "
        socket.send(password_test.encode())
        received_password = socket.recv(1024).decode()
        test = checkTextFile(received_user, received_password)
        if test == 1:
            connection_text = "+OK POP3 server is ready"
            socket.send(error_text.encode())
            return received_user
        else:
            error_text = "Wrong credentials, try again"
            socket.send(error_text.encode())

def getMailInfo(mail):
    lines = mail.strip().split("\n")
    info = []
    sender = lines[0]
    received = lines[3]
    subject = lines[2]
    info.append(sender)
    info.append(received)
    info.append(subject)
    return
def findMails(username):
    mailList = []
    with open(username + "/my_mailbox", "a") as myfile:
        #Doordat ik het "." niet mee in de mailbox steek, moet ik dit als splitsing
        # gebruiken, maar dan mogen er dus geen 2 lege lijnen in een mail zijn
        emails = myfile.read().strip().split("\n\n")
        for i in range(0, len(emails)):
            # Zodat ser_nr bij 1 start
            ser_nr = i + 1
            #Haal de sender, received & subject uit de mails
            lines = emails[i].strip().split("\n")
            info = []
            sender = lines[0]
            received = lines[3]
            subject = lines[2]
            info.append(ser_nr)
            info.append(sender)
            info.append(received)
            info.append(subject)
            mailList.append(info)
    return mailList
def main():
    # specify which port to listen on
    my_port = 12346
    # get the hostname of the server
    hostname = socket.gethostname()
    print(hostname)

    # create a socket
    my_socket = socket.socket()

    # bind the socket to the host and port
    my_socket.bind((hostname, my_port))
    print("binded")
    # wait for a connection, specify number of simultaneous clients
    my_socket.listen(1)
    print("done listening")
    # adress = IP-adress/host,port
    # Accept a connection.
    # The socket must be bound to an address and listening for connections.
    # The return value is a pair (conn, address) where conn is a new socket object
    # usable to send and receive data on the connection,
    # and address is the address bound to the socket on the other end of the connection.
    c, adress = my_socket.accept()
    print("accepted")
    print(f"Connected to: {adress}")

    while True:
        # Receive data from the client (up to 1024 bytes) and decode it
        text = c.recv(1024).decode()
        # If no data is received, break the loop
        if not text or text == "Exit":
            break
        print(f"Received from client: {text}")
        # Mail management
        if text == "Mail Management" or text == "2":
            user = userAuthentication(c)
            mailList = findMails(user)
            strList = str(mailList)
            c.send(strList.encode())

        # Mail Searching
        if text == "Mail Searching" or text == "3":
            option = c.recv(1024).decode()
            mailSearchingServer(c, option)
    c.close()
