Setup:

First start pop_server.py and mailserver_smtp.py
Than start mail_client.py

First fill in your username and password

After this you can choose what you would like to do
by entering associated number or the exact spelling of the option.
Tip: the number works much easier.




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

This is what you see at the server side

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