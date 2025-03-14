import os
import socket
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
    with open(user + "/my_mailbox", "a") as myfile:
        myfile.write(text)
        myfile.write("\n\n")
    return "OK"

def findAndAppendTime(full_message):
    local_time = time.localtime()
    string_local_time = time.strftime("%Y-%m-%d %H:%M", local_time)
    full_message.append("Received: " + string_local_time)

# berichten moeten hier in de volgende volgorde komen:
# 1 : MAIL FROM: <name@example.com>
# 2 : RCPT TO: <name@example.com>
# 3 : DATA <message>
# ontvangt enkel berichten en slaagt deze op. Stuurt geen berichten terug, enkel controlesignalen
def MailSendingServer(c, cs):
    while True:
        text = c.recv(1024).decode()
        if text.startswith("MAIL FROM:"):
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
                c.send((commands.get(-1) + " RCPT id not correct").encode())
                break
            # recipient not in database
            if username not in recipients:
                # send 550 ERROR
                c.send(commands.get(550).encode())
                break
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



def main():
    #specify which port to listen on
    my_port = 12345
    #get the hostname of the server
    hostname = socket.gethostname()

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
    print(f"Connected to: {adress}")
    #control signals
    cs = {"MAIL": "NOK",
          "RCPT": "NOK"}
    while True:
        # Receive data from the client (up to 1024 bytes) and decode it
        text = c.recv(1024).decode()
        # If no data is received, break the loop
        if not text or text == "Exit":
            break
        print(f"Received from client: {text}")
        # MAIL SENDING
        if text == "Mail Sending" or text == "1":
            MailSendingServer(c, cs)
        else:
            c.send(("Wrong input, try again").encode())
    c.close()



if __name__== "__main__":
    main()
