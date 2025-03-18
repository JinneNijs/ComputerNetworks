Setup:

The port for both servers are already specified inside the scripts. This is to make the testing easier. If necessary, this can be changed to input-based.

First start pop_server.py and mailserver_smtp.py
Than start mail_client.py

First fill in your username and password

After this you can choose what you would like to do
by entering associated number or the exact spelling of the option.
Tip: the number works much easier.

In general, when it says "S:" on the client side, it means you need to input something as the user.




This is an example of a mail being sent.
Important:
- You can only send emails with an e-mailadres that
has your username e.g.: username@domain"
If I would have used : From:Stan@kuleuven.be I would have received an error
- Use the domain specified by the server, here: kuleuven.be
- Don't put any spaces after "From:" or "To:" unless your username starts with a space
- You end your mail, by sending a "." on a single line
- The server checks your mail after this "." and gives back the appropriate control signals

This is what you see at the client side
"

Username? Jinne

Password? Jinne

Hello Jinne

Options:
 1) Mail Sending,
 2) Mail Management,
 3) Mail searching,
 4) Exit ?

 Enter number or name: 1

Server: 220 <kuleuven.be> Service ready

S: From:Jinne@kuleuven.be

S: To:Stan@kuleuven.be

S: Subject: Voorbeeld mail

S: Beste Stan

S: Dit is een voorbeeld.

S: Geniet ervan!

S: .

Server: 250 OK Hello kuleuven.be

Server: 250 OKsender ok

Server: 250 OK recipient ok

Server: 354 Intermediate reply Enter message, end with .:

Server: 250 OK message sent
"

This is what you see at the server side:
"
binded

done listening

Connected to: ('10.46.236.57', 52809)

Number of active clients: 1

Client: HELO kuleuven.be

Client: MAIL FROM: Jinne@kuleuven.be

Client: RCPT TO: Stan@kuleuven.be

Client: DATA

Client: From:Jinne@kuleuven.be

Client: To:Stan@kuleuven.be

Client: Subject: Voorbeeld mail

Client: Beste Stan

Client: Dit is een voorbeeld.

Client: Geniet ervan!

Client: .

Client: QUIT

Closed client connection
"

This is an example of how to perform Mail Management.
Important:
- You start by re-entering you USER and PASS to reassure that it is you who wants to manage your mails. This has to be the same user as the mail client.
- After that, you will receive your e-mails.
- Then you can enter the commands (STAT, RSET, QUIT, LIST (with a number or not), RETR and DELE (both with a number))
- When you enter an invalid command, you can just re-enter a new command
  
This is what you receive on the client side:
"
Hello Jinne
Options:
 1) Mail Sending,
 2) Mail Management,
 3) Mail searching,
 4) Exit ?
    
Enter number or name: 2

Server: +OK POP3 server is ready

Server: USER

S: Jinne

Server: PASS

S: Jinne

Server: [[1, 'From:Jinne@vtk.be', 'Received: 2025-03-17 16:31', 'Subject:1ste bericht'], [2, 'From:Jinne', 'Received: 2025-03-17 16:58', 'Subject: test multithreading'], [3, 'From:Stan@kuleuven.be', 'Received: 2025-03-17 20:21', 'Subject:test'], [4, 'From:Stan@kuleuven.be', 'Received: 2025-03-17 20:33', 'Subject:testing again'], [5, 'From:Stan@kuleuven.be', 'Received: 2025-03-17 20:39', 'Subject:test']]

Server: [[6, 'From:Stan@kuleuven.be', 'Received: 2025-03-17 20:45', 'Subject: test'], [7, 'From:Stan@kuleuven.be', 'Received: 2025-03-17 20:45', 'Subject: test2'], [8, 'From:Stan@kuleuven.be', 'Received: 2025-03-17 20:46', 'Subject:test3'], [9, 'From:Stan@kuleuven.be', 'Received: 2025-03-17 20:59', 'Subject:sjfsls'], [10, 'From:Stan@kuleuven.be', 'Received: 2025-03-17 21:07', 'Subject:wooo']]

Server: [[11, 'From:Stan@kuleuven.be', 'Received: 2025-03-18 08:43', 'Subject: threading'], [12, 'From:Jinne@kuleuven.be', 'Received: 2025-03-18 09:34', 'Subject:akakak'], [13, 'From:Stan@kuleuven.be', 'Received: 2025-03-18 09:39', 'Subject: no text'], [14, 'From:Stan@kuleuven.be', 'Received: 2025-03-18 09:40', 'Subject: no text2']]

Command? STAT

Server: +OK 14 2090

Command? LIST 7

Server: +OK 7 141

Command? RETR 7

Server: +OK 141 octets

Server: ['From:Stan@kuleuven.be\n', 'To:Jinne@kuleuven.be\n', 'Subject: test2\n', 'Received: 2025-03-17 20:45\n', 
'sflsde\n']

Server: .

Command? DELE 7

Server: +OK message 7 deleted

Command? LIST 7

Server: ERROR no message with this number (or has been deleted)

Command? DELE 7

Server: -ERR message 7 already deleted

Command? LIST 20

Server: ERROR no message with this number (or has been deleted)

Command? RSET

Server: +OK maildrop has 14 messages (1467 octets)

Command? LIST 7

Server: +OK 7 141

Command? DELE 5

Server: +OK message 5 deleted

Command? DELE 6

Server: +OK message 6 deleted

Command? STAT

Server: +OK 12 1809

Command? QUIT

Server: +OK pop3 server signing off (Number of messages left : 12)
"

This is an example of Mail Searching:
Important: 
- if your search term is not inside one of the mails. Your output will be empty.
- Both "1)" and "1" work within the mail searching.
Hello Jinne
Options:
 1) Mail Sending,
 2) Mail Management,
 3) Mail searching,
 4) Exit ?
 Enter number or name: 3

How would you like to search:

1) Words/sentences, 2) Time, 3) Address ? Enter the number (for example "1)" ): 1

Words/sentences input: 1ste

output:

['From:Jinne@vtk.be', 'To:Jinne@vtk.be', 'Subject:1ste bericht', 'Received: 2025-03-17 16:31', 'Dit is het 1ste bericht']
