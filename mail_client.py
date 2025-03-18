import socket
import time


def checkMessageFormat(message_list):

    if len(message_list) < 4:
        return False
    elif message_list[0].startswith("From:") and message_list[1].startswith("To:") and message_list[2].startswith("Subject:"):
        return True
    else:
        return False
def checkDomain(message_list,domain):
    bl_from = False
    bl_to = False

    index_from = int(message_list[0].find("@"))
    domain_from = message_list[0][index_from+1:]
    if domain_from== domain:
        bl_from = True

    index_to = int(message_list[1].find("@"))
    domain_to = message_list[1][index_to + 1:]
    if domain_to == domain:
        bl_to= True
    return bl_from*bl_to

def findToMail(text):

    username = text[3:]
    return username
def findFromMail(text):
    username = text[5:]
    return username
def checkSender(user_email,username):
    index_at = int(user_email.find("@"))
    if user_email[5:index_at]==username:
        return True
    return False
# send mails to the mailserver socket, using SMTP protocol
# berichten moeten hier in de volgende volgorde verstuurd worden en in dit formaat:
# 1 : MAIL FROM: <name@example.com>
# 2 : RCPT TO: <name@example.com>
# 3 : DATA <message>
def MailSendingClient(username):
    smtp_port = 12345
    s = socket.socket()
    hostname = socket.gethostname()
    s.connect((hostname, smtp_port))
    domain = s.recv(1024).decode()
    print(f"Server: 220 <{domain}> Service ready")
    message = ""
    while True:
        message_str = input('S: ')

        if message_str == ".":
            message = message + message_str
            message_list = message.split("\n")

            correctFormat = checkMessageFormat(message_list)
            if correctFormat:
                #check that sender is the mailcient
                if checkSender(message_list[0], username):

                    #second check domains
                    correctDomain = checkDomain(message_list,domain)
                    if correctDomain:
                        s.send((f"HELO {domain}").encode())
                        received= s.recv(1024).decode()
                        print(f"Server: {received}")

                        if received == f"250 OK Hello {domain}":
                            s.send((f"MAIL FROM: {findFromMail(message_list[0])}").encode())
                            received = s.recv(1024).decode()
                            print(f"Server: {received}")
                            if received.startswith("250"):
                                s.send((f"RCPT TO: {findToMail(message_list[1])}").encode())
                                received = s.recv(1024).decode()
                                print(f"Server: {received}")

                                if received.startswith("250"):
                                    s.send((f"DATA").encode())
                                    received = s.recv(1024).decode()
                                    print(f"Server: {received}")

                                    if received.startswith("354"):
                                        for line in message_list:
                                            s.send((line).encode())
                                            time.sleep(0.5)
                                        received = s.recv(1024).decode()
                                        print(f"Server: {received}")

                                        if received.startswith("250"):
                                            s.send(("QUIT").encode())
                                            received = s.recv(1024).decode()
                                            print(f"Server: {received}")
                                            return
                                else:
                                    print("550 No such user. Try again from scratch")
                                    continue

                            else:
                                message =""
                                print("550 No such user. Try again from scratch")
                                continue
                    else:
                        message = ""
                        print("Wrong domain")
                        continue
                else:
                    message = ""
                    print("Cannot send mails from different account, please use your own e-mail")
                    continue


            else:
                print("wrong format please try again")
                continue
        message = message + message_str +"\n"



#doet hetzelfde als findMails, maar houdt nu de volledige mails bij
def findFullMails(username):
    mailList = []
    current_mail = []
    with open(username + "/my_mailbox.txt", "r") as myfile:
        # Read file line by line
        line = myfile.readline()
        ser_nr = 1
        while line:
            line = line.strip()  # Clean up the line
            if line == "":  # Empty line marks the end of the current email
                # Only process mail if there's data collected
                if current_mail:

                    # Add to mailList with the serial number
                    mailList.append(current_mail)
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

# full implementation for MailSearching
def MailSearchingClient(option, username):
    #Searching for words
    if option == "1)":
        words = input('Words/sentences input: ')
    #Searching for date
    if option == "2)":
        words = input('Date (MM/DD/YY): ')
    #Searching for address
    if option == "3)":
        words = input('Email address: ')
    print("output:")
    #lijst met de volledige mails
    maillist = findFullMails(username)
    #option 1 = words/sentences
    for mail in maillist:
        # option 1 = words/sentences
        if option == "1)":
            # For every element inside mail (so for From:..., To:..., Subject:..., etc.)
            for i in range(0,len(mail)):
                if words in mail[i]:
                    #Voeg het message-gedeelte samen in 1 item in de lijst in plaats van dat elke aparte lijn 1 lijstitem is
                    processed_email = mail[:4] + ['\n'.join(mail[4:])]
                    print(processed_email)
                    break
        # option 2 = date
        if option == "2)":
            date = words.split("/")
            month = date[0]
            day = date[1]
            year = date[2]
            # change date to same format as in mails
            right_date = "20" + year + "-" + month + "-" + day
            if right_date in mail[3]:
                #Voeg het message-gedeelte samen in 1 item in de lijst in plaats van dat elke aparte lijn 1 lijstitem is
                processed_email = mail[:4] + ['\n'.join(mail[4:])]
                print(processed_email)
        if option == "3)":
            if words in mail[0]:
                #Voeg het message-gedeelte samen in 1 item in de lijst in plaats van dat elke aparte lijn 1 lijstitem is
                processed_email = mail[:4] + ['\n'.join(mail[4:])]
                print(processed_email)
    return



# om mails van een persoon te managen
def MailManagementClient(username):
    hostname = socket.gethostname()

    pop3_port = 12346
    pop_socket = socket.socket()
    pop_socket.connect((hostname, pop3_port))
    str_mm = "Mail Management"
    pop_socket.send(str_mm.encode())
    # The part for the authentication
    while True:
        received = pop_socket.recv(1024).decode()
        print(f"Server: {received}")
        # command QUIT has been enterd, get out of managment system
        if "signing off" in received:
            break
        # pop server will ask for authentication
        if received == "USER" :
            str = input('S: ')
            if str == username:
                pop_socket.send(str.encode())
            else:
                print("USER does not match client login, please use your own username")
                pop_socket.send("wrong user".encode())
        elif  received == "PASS":
            str = input('S: ')
            pop_socket.send(str.encode())
        elif received.startswith("Wrong credentials"):
            continue
        elif received.startswith("["):
            while True:
                received = pop_socket.recv(1024).decode()
                if received ==".":
                    break
                print(f"Server: {received}")
            #current_maillist = received
            #If the mailing list is received, go on to the management part where you can enter commands like STAT
            #Dus verderwerken met die current_maillist om daar commands op uit te voeren?
            while True:
                command = input("Command? ")
                command = command.upper()
                pop_socket.send(command.encode())
                #stat en dele moeten zelfde doen
                if command == "STAT" or command.startswith("DELE") or command == "RSET":
                    received = pop_socket.recv(1024).decode()
                    print(f"Server: {received}")
                if command.startswith("LIST"):
                    if len(command)> len("LIST"):
                        received = pop_socket.recv(1024).decode()
                        print(f"Server: {received}")
                    else:
                        while True:
                            received = pop_socket.recv(1024).decode()
                            print(f"Server: {received}")
                            if received == ".":
                                break
                if command.startswith("RETR"):
                    while True:
                        received = pop_socket.recv(1024).decode()
                        print(f"Server: {received}")
                        if received == "-ERR no such message":
                            break
                        if received == ".":
                            break
                if command == "QUIT":
                    received = pop_socket.recv(1024).decode()
                    print(f"Server: {received}")
                    break
            break




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


def main():
    # definier poort, vindt hostname en maak een socket aan
    # bind de socket aan de poort en hostname
    # analoog voor de pop server


    while True:
        # vraag name en passwoord op
        username = input("Username? ")
        password = input("Password? ")
        # checks if user and password are know and valid, returns 1 if true, 0 if not
        test = checkTextFile(username,password)
        if test == 1:
            break
        print("Wrong Username or Password. Please try again!")
    while True:
        # geef alle opties aan de klant voor het beheren van zijn mailbox
        str = input('Hello ' + username + '\nOptions:\n 1) Mail Sending,\n 2) Mail Management,\n 3) Mail searching,\n 4) Exit ?\n Enter number or name: ')
        if str == "Exit" or str == "4":
            break
            # Optie 1 : mail sending
        if str == "Mail Sending" or str == "1":
            MailSendingClient(username)
            # Optie 2 : mail managment
        if str == "Mail Management" or str == "2":
            MailManagementClient(username)
            # Optie 3: mail searching
        if str == "Mail Searching" or str == "3":
            #Vraag, moet je voor mail searching eerst mail management gedaan hebben (en ingelogd zijn?) Zo ja, werken met commands zoals bij mail sending?

            option = input('How would you like to search: 1) Words/sentences, 2) Time, 3) Address ? Enter the number (for example "1)" ): ')

            MailSearchingClient(option, username)




if __name__== "__main__":
    main()