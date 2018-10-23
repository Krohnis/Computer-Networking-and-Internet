from socket import *

#SocketPort and binding
serverPort = 80
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
	#Shows that server is listening
	print 'Ready to serve...'
	connectionSocket, addr = serverSocket.accept()

	try:
		message = connectionSocket.recv(1024)
		print message
		
		#Display for when port 80 is called
		connectionSocket.send("<h1>CSC138</h1>")

		#For files, displays HTML file when present, otherwise goes to 404
		filename = message.split()[1]
		f = open(filename[1:])
		outputdata = f.read()
		print outputdata
		connectionSocket.send('\nHTTP/1.1 200 OK\n')
		connectionSocket.send('Connection: close\n')
		LengthString = 'Connection-Length:' + str(len(outputdata)) + '\n\n'
		connectionSocket.send(';Content-Type: text/html\n\n')
		connectionSocket.send(outputdata)
		connectionSocket.close()
	except IOError:
		#Displays 404 Error when requested file is not present
		Message404 = '404 Not Found: ' + filename + '\n'
		connectionSocket.send(Message404)
		connectionSocket.close()

serverSocket.close()