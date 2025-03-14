import socket

def MailSendingClient(client_socket):
    while True:
        str = input('S: ')
        client_socket.send(str.encode())
        received_text = client_socket.recv(1024).decode()
        print(f"N: {received_text}")
        if received_text.startswith("354"):
            while True:
                message_str = input('S: ')
                client_socket.send(message_str.encode())
                if message_str == ".":
                    received_text = client_socket.recv(1024).decode()
                    if received_text.startswith("250"):
                        print(f"N: {received_text}" + ", Message sent")
                        return
                    else:
                        print("ERROR: Start over with MAIL FROM")
                        break
        if received_text == "ERROR":
            break

def MailSearchingClient(socket, option):
    #Searching for words
    if option == "1)":
        words = input('Words/sentences input: ')
    #Searching for date
    if option == "2)":
        words = input('Date (MM/DD/YY): ')
    #Searching for address
    if option == "3)":
        words = input('Email address: ')

    socket.send(words.encode())
    while True:
        mail = socket.recv(1024).decode()
        if mail.startswith("From:"):
            print("{" + mail + "}")
        else:
            break
    return


def MailManagementClient(socket):
    # The part for the authentication
    while True:
        received = socket.recv(1024).decode()
        print(f"N: {received}")
        if "signing off" in received:
            break
        if received == "USER" or received == "PASS":
            str = input('S: ')
            socket.send(str.encode())
        elif received.startswith("Wrong credentials"):
            continue
        elif received.startswith("["):
            current_maillist = received
            #If the mailing list is received, go on to the management part where you can enter commands like STAT(which I haven't written yet)
            #Dus verderwerken met die current_maillist om daar commands op uit te voeren?
            while True:
                command = input("Command? ")
                socket.send(command.encode())
                if command == "STAT":
                    received = socket.recv(1024).decode()
                    print(f"N: {received}")
                if command.startswith("LIST"):
                    if len(command)> len("LIST"):
                        received = socket.recv(1024).decode()
                        print(f"N: {received}")
                    else:
                        while True:
                            received = socket.recv(1024).decode()
                            print(f"N: {received}")
                            if received == ".":
                                break

                if command == "QUIT":
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
    smtp_port = 12345
    smtp_socket = socket.socket()
    hostname = socket.gethostname()
    smtp_socket.connect((hostname,smtp_port))

    pop3_port = 12346
    pop3_socket = socket.socket()
    pop3_socket.connect((hostname,pop3_port))
    while True:
        username = input("Username? ")
        password = input("Password?")
        # checks if user and password are know and valid, returns 1 if true, 0 if not
        test = checkTextFile(username,password)
        if test == 1:
            break
        print("Wrong Username or Password. Please try again!")
    while True:

        str = input('Hello '+ username + '\nOptions:\n 1)Mail Sending,\n 2) Mail Management,\n 3) Mail searching,\n 4) Exit ?\n Enter number or name: ')
        if str == "Exit" or str == "4":
            break
        if str == "Mail Sending" or str == "1":
            smtp_socket.send(str.encode())
            MailSendingClient(smtp_socket)
        if str == "Mail Management" or str == "2":
            pop3_socket.send(str.encode())
            MailManagementClient(pop3_socket)
        if str == "Mail Searching" or str == "3":
            #Vraag, moet je voor mail searching eerst mail management gedaan hebben (en ingelogd zijn?) Zo ja, werken met commands zoals bij mail sending?
            pop3_socket.send(str.encode())
            option = input('How would you like to search: 1) Words/sentences, 2) Time, 3) Address ? Enter the number (for example "1)" ): ')
            pop3_socket.send(option.encode())
            MailSearchingClient(pop3_socket,option)


    smtp_socket.close()
    pop3_socket.close()

if __name__== "__main__":
    main()