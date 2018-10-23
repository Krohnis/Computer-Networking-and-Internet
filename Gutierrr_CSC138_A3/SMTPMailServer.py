from socket import *

#Selects the mail server and assigns it to mailServer
mailserver = "localhost"
#Select the socket number and assigns it to mailPort
serverport = 25

#Creates the connecting socket and connects it to the mailServer
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, serverport))
recv = clientSocket.recv(1024)
print recv
if recv[:3] != '220':
    print '220 reply not received from server.'

#Identifies that a connection has been made between client and server
print 'Sending HELLO Command'
helloCommand = 'HELLO Professor\r\n'
clientSocket.send(helloCommand)
recv1 = clientSocket.recv(1024)
print recv1
if recv1[:3] != '250':
    print '250 reply not received from server.\n'

#Fills the textfield for sender in the email header
print 'Sending MAIL FROM Command'
mailFromCommand = 'Mail From: rickygutierrez@csus.edu\r\n'
clientSocket.send(mailFromCommand)
recv2 = clientSocket.recv(1024)
print recv2
if recv1[:3] != '250':
    print '250 reply not received from server.\n'

#Fills the textfield for the receiver in the email header
print 'Sending RCPT TO Command'
rcptToCommand = 'RCPT to: rickygutierrez@csus.edu\r\n'
clientSocket.send(rcptToCommand)
recv3 = clientSocket.recv(1024)
print recv3
if recv1[:3] != '250':
    print '250 reply not received from server.\n'

#Sends DATA Command
print 'Sending DATA Command'
dataCommand = 'DATA to: rickygutierrez@csus.edu\r\n'
clientSocket.send(dataCommand)
recv4 = clientSocket.recv(1024)
print recv4
if recv1[:3] != '354':
    print '250 reply not received from server.\n'

#Send message data
print "Sending MESSAGE Command"
msg = "SUBJECT: CSC138\nCSC138, Assignment 3, Submission\n.\r\n"
clientSocket.send(msg)
recv1 = clientSocket.recv(1024)
print recv1
if recv1[:3] != '250':
    print '250 reply not received from server.\n'

#Send QUIT command and get server response.
print 'Sending QUIT Command'
clientSocket.send('QUIT\r\n')
recv6 = clientSocket.recv(1024)
print recv6
if recv6[:3] != '221':
    print '221 reply not received from server.\n'
clientSocket.close()