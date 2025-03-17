import os
import threading
import socket
import sys
import time
from fileinput import close

#COMMANDS
commands = {250: "250 OK",
            -1: "ERROR",
            550: "550 No such user",
            354: "354 Intermediate reply"}

def findUsername(text):

    index_at = int(text.find('@'))
    if index_at == -1:
        return 0
    Username = text[:index_at]
    return Username

#bericht ontvangen is van de vorm : MAIL FROM: <name@example.com>
#geeft name terug
def findReversePath(text):
    index_from = int(text.find('FROM:'))
    if index_from==-1:
        return "/"
    #text van de vorm MAIL FROM:<reversepath>
    rp = text[index_from+5:]
    return rp
#bericht ontvangen is van de vorm : TO: <name@example.com>
#geeft name terug
def findForwardPath(text):
    index_from = int(text.find('TO:'))
    if index_from == -1:
        return "/"
    # text van de vorm RCPT TO:<forwardpath>
    fp = text[index_from + 3:]
    return fp

def findRecipients():
    recipients = set()
    with open("userinfo.txt") as file:
        #read all lines of the file
        lines = file.readlines()
        for line in lines:
            #if line starts with space, end of file
            if line.startswith(" "):
                break
            #separate user from password
            recipient = line.split()[0]
            #store user in set
            recipients.add(recipient)
    file.close()
    return recipients



def storeMessage(user,text):
    #look for stop signal and returns actual message
    #store in mailbox of user
    with open(user + "/my_mailbox.txt", "a") as myfile:
        myfile.write(text)
        myfile.write("\n\n")
    return "OK"

def findAndAppendTime(full_message):
    local_time = time.localtime()
    string_local_time = time.strftime("%Y-%m-%d %H:%M", local_time)
    full_message.append("Received: " + string_local_time)

def checkMessageFormat(message):

    if len(message) < 5:
        return 0
    elif message[0].startswith("From:") and message[1].startswith("To:") and message[2].startswith("Subject:"):
        return 1
    else: return 0

# berichten moeten hier in de volgende volgorde komen:
# 1 : MAIL FROM: <name@example.com>
# 2 : RCPT TO: <name@example.com>
# 3 : DATA <message>
# ontvangt enkel berichten en slaagt deze op. Stuurt geen berichten terug, enkel controlesignalen
def MailSendingServer(c, cs):
    while True:

        text = c.recv(1024).decode()
        if text.startswith("HELO"):
            cs["HELO"] = "NOK"
            if text[4:] == " vtk.be":
                c.send((commands.get(250) + f" Hello vtk.be").encode())
                cs["HELO"]= "OK"
            else:
                c.send((commands.get(-1) +" wrong domain").encode())
        elif text.startswith("MAIL FROM:") and cs["HELO"]=="OK":
            # clear out buffers etc..
            cs["MAIL"] = "NOK"
            cs["RCPT"] = "NOK"
            #find the sender of the mail = person to sent back to
            rp = findReversePath(text)
            # no reversepath found: "/" control signal
            if rp == "/":
                # send ERROR
                c.send(commands.get(-1).encode())
                break
            # reverspath ok, send 250 ok
            c.send(commands.get(250).encode())
            # UPDATE CONTROLSIGNAL
            cs["MAIL"] = "OK"
        # RCPT
        # check also that MAIL procedure has been gone through
        elif text.startswith("RCPT TO:") and cs.get("MAIL") == "OK":

            fp = findForwardPath(text)
            username = findUsername(fp)
            # find all possible recipients at this given moment
            recipients = findRecipients()
            # if no forwardpath is found
            if fp == "/":
                c.send((commands.get(-1) + " RCPT format incorrect").encode())
                break
            # recipient not in database
            if username not in recipients:
                # send 550 ERROR
                c.send(commands.get(550).encode())
                continue
            # forwardpath found and recipient ok
            # send 250 ok
            c.send(commands.get(250).encode())
            cs["RCPT"] = "OK"
        # DATA
        elif text.startswith("DATA") and cs.get("RCPT") == "OK":
            # . is our STOP signal
            c.send((commands.get(354) + " Enter message, end with .: ").encode())
            # receive message
            full_message = []
            while True:
                message_line = c.recv(1024).decode()
                if message_line == ".":
                    break
                full_message.append(message_line)
                # Na de subject line, vind de tijd en voeg deze toe aan de message
                if message_line.startswith("Subject:"):
                    findAndAppendTime(full_message)
            # put all the lines in 1 string and seperate them with new line
            check = checkMessageFormat(full_message)
            if check == 0:
                c.send((commands.get(-1) + "wrong message format used, please try again").encode())
                continue
            message = "\n".join(full_message)

            # store message in mailbox of username
            cs = storeMessage(username, message)
            # if stored, send 250 ok
            if cs == "OK":
                c.send(commands.get(250).encode())
            # end of mail
            return
        else:
            c.send((commands.get(-1)+ "wrong format used, please try again").encode())


def startSMTPServer():
    # specify which port to listen on
    my_port = 12345
    # get the hostname of the server
    hostname = socket.gethostname()

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
    while True:
        c, adress = my_socket.accept()
        clientThread = threading.Thread(target=main, args=[c])
        clientThread.start()
        print(f"Connected to: {adress}")
        print(f"Number of active clients: {threading.active_count() - 1}")

def main(c):

    #control signals
    cs = {"HELO" : "NOK",
          "MAIL": "NOK",
          "RCPT": "NOK"}
    while True:
        # Receive data from the client (up to 1024 bytes) and decode it
        c.send((f"220 <{DOMAIN}>").encode())
        # If no data is received, break the loop
        # MAIL SENDING
        MailSendingServer(c, cs)
    c.close()

DOMAIN = "kuleuven.be"

if __name__== "__main__":
    startSMTPServer()
