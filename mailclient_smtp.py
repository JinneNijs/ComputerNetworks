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




def main():
    smtp_port = 12345
    smtp_socket = socket.socket()
    hostname = socket.gethostname()
    smtp_socket.connect((hostname,smtp_port))

    pop3_port = 12346
    pop3_socket = socket.socket()
    pop3_socket.connect((hostname,pop3_port))

    while True:
        str = input('Option: 1)Mail Sending, 2) Mail Management, 3) Mail searching, 4) Exit ? Enter number or name: ')
        if str == "Exit" or str == "4":
            break
        if str == "Mail Sending" or str == "1":
            smtp_socket.send(str.encode())
            MailSendingClient(smtp_socket)
        if str == "Mail Searching" or str == "3":
            pop3_socket.send(str.encode())
            option = input('How would you like to search: 1) Words/sentences, 2) Time, 3) Address ? Enter the number (for example "1)" ): ')
            pop3_socket.send(option.encode())
            MailSearchingClient(pop3_socket,option)
        if str == "Mail Management" or str == "2":
            smtp_socket.send(str.encode())
            #MailManagementClient()

    smtp_socket.close()
    pop3_socket.close()

if __name__== "__main__":
    main()