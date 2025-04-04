
import threading
import socket
import time


# COMMANDS
commands = {250: "250 OK",
            -1: "ERROR",
            550: "550 No such user",
            354: "354 Intermediate reply"}

# starts with: name@example.com and gives back name
def findUsername(text):

    index_at = int(text.find('@'))
    if index_at == -1:
        return "/"
    Username = text[1:index_at]
    return Username

# bericht ontvangen is van de vorm : MAIL FROM: <name@example.com>
# geeft name@example.com terug
def findReversePath(text):
    index_from = int(text.find('FROM:'))
    if index_from==-1:
        return "/"
    # text van de vorm MAIL FROM:<reversepath>
    rp = text[index_from+5:]
    return rp
# bericht ontvangen is van de vorm : ...TO: <name@example.com>
# geeft name@example.com terug
def findForwardPath(text):
    index_from = int(text.find('TO:'))
    if index_from == -1:
        return "/"
    # text van de vorm RCPT TO:<forwardpath>
    fp = text[index_from + 3:]
    return fp

# give back the users out of the userinfo.txt file
def findRecipients():
    recipients = []
    with open("userinfo.txt") as file:
        # read all lines of the file
        lines = file.readlines()
        for line in lines:
            # if line starts with space, end of file
            if line.startswith(" "):
                break
            # separate user from password
            recipient = line.split()[0]
            # store user in set
            recipients.append(recipient)
    file.close()
    return recipients


def storeMessage(user,text):
    #store in mailbox of user
    with open(user + "/my_mailbox.txt", "a") as myfile:
        myfile.write(text)
        myfile.write("\n\n")
    return "OK"

# add the time to the message
def findAndAppendTime(full_message):
    local_time = time.localtime()
    string_local_time = time.strftime("%Y-%m-%d %H:%M", local_time)
    full_message.append("Received: " + string_local_time)


# Berichten moeten hier in de volgende volgorde komen:
# 1 : MAIL FROM: <name@example.com>
# 2 : RCPT TO: <name@example.com>
# 3 : DATA <message>
# ontvangt enkel berichten en slaagt deze op. Stuurt geen berichten terug, enkel controlesignalen
def MailSendingServer(c, cs):
    try:
        while True:
            text = c.recv(1024).decode()
            print(f"Client: {text}")
            if text.startswith("HELO"):
                cs["HELO"] = "NOK"
                # check the domain
                if text[5:] == DOMAIN:
                    c.send((commands.get(250) + f" Hello {DOMAIN}").encode())
                    # turn the control signal to OK
                    cs["HELO"]= "OK"
                else:
                    c.send((commands.get(-1) + " wrong domain").encode())
            elif text.startswith("MAIL FROM:") and cs["HELO"] == "OK":
                # clear out buffers etc..
                cs["MAIL"] = "NOK"
                cs["RCPT"] = "NOK"
                # find the sender of the mail = person to sent back to
                rp = findReversePath(text)
                rp = findUsername(rp)
                # find all usernames inside the userinfo.txt file
                recipients = findRecipients()
                # no reversepath found: "/" control signal
                if rp == "/":
                    # send ERROR
                    c.send(commands.get(-1).encode())
                    break
                if rp not in recipients:
                    # send 550 ERROR
                    c.send(commands.get(550).encode())
                    continue
                # reverspath ok, send 250 ok
                c.send((commands.get(250) + " sender ok").encode())
                # UPDATE CONTROLSIGNAL
                cs["MAIL"] = "OK"
            # RCPT
            # check also that MAIL procedure has been gone through
            elif text.startswith("RCPT TO:") and cs.get("MAIL") == "OK":
                #find username of recipient
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
                c.send((commands.get(250)+" recipient ok").encode())
                cs["RCPT"] = "OK"
            # DATA
            elif text.startswith("DATA") and cs.get("RCPT") == "OK":
                # . is our STOP signal
                c.send((commands.get(354) + " Enter message, end with .: ").encode())
                # receive message
                full_message = []
                # Receive all the message lines
                while True:
                    message_line = c.recv(1024).decode()
                    print(f"Client: {message_line}")
                    if message_line == ".":
                        break
                    full_message.append(message_line)
                    # After subject line, find the tijd and add it
                    if message_line.startswith("Subject:"):
                        findAndAppendTime(full_message)
                # put all the lines in 1 string and seperate them with new line
                message = "\n".join(full_message)

                # store message in mailbox of username
                cs = storeMessage(username, message)
                # if stored, send 250 ok
                if cs == "OK":
                    c.send((commands.get(250) + " message sent").encode())
                # end of mail
            elif text == "QUIT":
                break
    except ConnectionResetError:
        print("Client forcefully closed the connection.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        c.close()
        print("Closed client connection")


# Start of the file
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
        #start a new thread to perform main
        clientThread = threading.Thread(target=main, args=(c,))
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
        c.send((f"{DOMAIN}").encode())
        # If no data is received, break the loop
        # MAIL SENDING
        MailSendingServer(c, cs)
        return


DOMAIN = "kuleuven.be"

if __name__ == "__main__":
    startSMTPServer()
