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


def main():
    client_port = 12345
    client_socket = socket.socket()
    hostname = socket.gethostname()
    client_socket.connect((hostname,client_port))

    while True:
        str = input('Option: 1)Mail Sending, 2) Mail Management, 3) Mail searching, 4) Exit ? Enter number or name: ')
        if str == "Exit" or str == "4":
            break
        if str == "Mail Sending" or str == "1":
            client_socket.send(str.encode())
            MailSendingClient(client_socket)

    client_socket.close()

if __name__== "__main__":
    main()