import socket
import time
from fileinput import close
import pickle
import sys


#vraagt user en password in terminal
def checkTextFile(user, password):
    with open("userinfo.txt") as file:
        # read all lines of the file for user and passwords
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
                    #als alles klopt, return 1
                    return 1
    file.close()
    #user /password niet in file  of fout
    return 0

#vraagt username en password en kijkt of deze kloppen
def userAuthentication(socket):
    while True:
        user_text = "USER"
        socket.send(user_text.encode())
        received_user = socket.recv(1024).decode()
        if received_user == "QUIT":
            socket.send(("+OK POP3 server signing off").encode())
            return "quit"
        password_text = "PASS"
        socket.send(password_text.encode())
        received_password = socket.recv(1024).decode()
        if received_password == "QUIT":
            socket.send(("+OK POP3 server signing off").encode())
            return "quit"
        #checks if user and password are know and valid, returns 1 if true, 0 if not
        test = checkTextFile(received_user, received_password)
        if test == 1:
            connection_text = "+OK POP3 server is ready"
            socket.send(connection_text.encode())
            #als user en password kloppen, return username
            return received_user
        else:
            # anders try again
            error_text = "Wrong credentials, try again"
            socket.send(error_text.encode())

#voor mail management: splitst mailbox om te sturen naar client
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
    current_mail = []
    with open(username + "/my_mailbox", "r") as myfile:
        # Read file line by line
        line = myfile.readline()
        ser_nr = 1
        while line:
            line = line.strip()  # Clean up the line
            if line == "":  # Empty line marks the end of the current email
                # Only process mail if there's data collected
                if current_mail:
                    # Extract the sender, subject, and received details
                    sender = current_mail[0]
                    subject = current_mail[2]
                    received = current_mail[3]

                    # Add to mailList with the serial number
                    mailList.append([ser_nr, sender, received, subject])
                    current_mail = []  # Reset for the next mail

                    ser_nr += 1  # Increment serial number for next email
                else:
                    break
            else:
                # Collect the current mail's lines
                current_mail.append(line)

            # Read the next line
            line = myfile.readline()

    return mailList
def performSTAT(maillist,username):
    with open(username +"/my_mailbox","r") as myfile:
        message ="".join(myfile.readlines())
        bytes = sys.getsizeof(message)
    myfile.close()
    length = findNumberOfMessages(maillist)
    return length, bytes

def findNumberOfMessages(list):
    length = len(list)
    return length

def scanListing(user):

    numbers_bytes = []
    message= ""
    with open(user+"/my_mailbox",'r') as myfile:

        while True:
            line = myfile.readline()
            if line == "":
                break
            if line == "\n":
                numbers_bytes.append(sys.getsizeof(message))
                message = ""
                continue
            message += line


    myfile.close()
    return numbers_bytes




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

            #checkt username en password
            user = userAuthentication(c)
            if user == "quit":
                continue
            #verzamelt alle eerder gekregen mails van de user in een geordende lijst
            mailList = findMails(user)
            strList = str(mailList)
            #geeft de mails terug aan de client
            c.send(strList.encode())
            deleted_mails = []
            while True:
                command = c.recv(1024).decode()
                bytes = scanListing(user)
                total = len(bytes)
                if command == "STAT":
                    c.send((f"+OK {len(bytes)} {sum(bytes)}").encode())
                elif command.startswith("LIST"):

                    if command == "LIST":
                        c.send((f"+OK {len(bytes)} {sum(bytes)}").encode())
                        for nr in range(0,len(bytes)):
                            c.send((f"+OK {nr+1} {bytes[nr]}").encode())
                            time.sleep(1)
                        time.sleep(1)
                        c.send(".".encode())
                    else:
                        command, nr = command.split()
                        nr= int(nr)
                        if nr > total:
                            c.send(("ERROR nr is bigger than number of messages").encode())
                        c.send((f"+OK {nr} {bytes[nr-1]}").encode())
                elif command.startswith("RETR"):
                    if command == "RETR":
                        c.send(("-ERR no message number attached").encode())
                    else:
                        command, nr = command.split()
                        total = findNumberOfMessages(mailList)
                        nr = int(nr)
                        if nr > total:
                            c.send(("-ERR no such message").encode())
                        #hier moet eerst de grootte van die ene mail gevonden worden en dan de message doorgegeven worden (zie rfc)
                        #eindigen door een punt door te sturen
                elif command.startswith("DELE"):
                    if command == "DELE":
                        c.send(("-ERR no message number attached").encode())
                    else:
                        command, nr = command.split()
                        total = findNumberOfMessages(mailList)
                        nr = int(nr)
                        if nr > total:
                            c.send(("-ERR no such message").encode())
                        else:
                            if nr in deleted_mails:
                                c.send((f"-ERR message {nr} already deleted").encode())
                            else:
                                #lijst bijhouden en deze dan gebruiken bij QUIT om ze uit mymailbox te verwijderen
                                deleted_mails.append(nr)
                                c.send((f"+OK message {nr} deleted").encode())
                elif command == "RSET":
                    #lijst terug nul maken
                    deleted_mails = []
                    total, bytes = performSTAT(mailList,user)
                    c.send((f"+OK maildrop has {total} messages ({bytes} octets)").encode())
                elif command == "QUIT":
                    # remove all messages markes as delete TO DO
                    nmbrOfMess = str(findNumberOfMessages(mailList))
                    c.send(("+OK pop3 server signing off (Number of messages left : "+ nmbrOfMess +")").encode())
                    break

        # Mail Searching
    c.close()

if __name__== "__main__":
    main()