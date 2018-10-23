from socket import *
import os
import sys
import struct
import time
import select
import binascii
import socket
ICMP_ECHO_REQUEST = 8

#Provided by the skeleton code
def checksum(str):
	csum = 0
	countTo = (len(str) / 2) * 2
	count = 0
	while count < countTo:
		thisVal = ord(str[count+1]) * 256 + ord(str[count])
		csum = csum + thisVal
		csum = csum & 0xffffffffL
		count = count + 2
	if countTo < len(str):
		csum = csum + ord(str[len(str) - 1])
		csum = csum & 0xffffffffL
	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)
	answer = ~csum
	answer = answer & 0xffff
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer

def receiveOnePing(clientSocket, ID, timeout, destAddr):
	timeLeft = timeout
	while 1:
		startedSelect = time.time()
		whatReady = select.select([clientSocket], [], [], timeLeft)
		howLongInSelect = (time.time() - startedSelect)
		if whatReady[0] == []:
			return "Request Timed Out"
		timeReceived = time.time()
		recPacket, addr = clientSocket.recvfrom(1024)
		#Fill in start
		#Fetch the ICMP header from the IP packet
		#Determines the time that the packet was sent
		timeSent = struct.unpack('d', recPacket[28:])
		#Determines 'round-trip-time' by substracting the time received and the time sent
		roundTripTime = (timeReceived - timeSent) * 1000
		#Unpacks the packet, and retrieves the IP address, assigns to IP_Addr
		IP_Addr = struct.unpack('!BBHHHBBH4s4s', recPacket[:20])
		#Gets the 'time-to-live' of the packet
		timeToLive = IP_Addr[5]
		#Converts the 32-bit packed IPv4 address to the standard
		addr = socket.inet_ntoa(IP_Addr[8])
		#Sets bytes to the length of the received packet
		bytes = len(recPacket)
		#Print statement that prints the necessary outputs to screen
		return 'Reply from {}: bytes={}, time={}ms, TTL={}'.format(addr, bytes, roundTripTime, timeToLive)

		#Fill in end
		timeLeft = timeLeft - howLongInSelect
		if timeLeft <= 0:
			return "Request Timed Out"

def sendOnePing(clientSocket, destAddr, ID):
	#Header is type (8), code (8), checksum (16), id (16), sequence (16)
	global packageSent
	#Make a dummy header with a 0 checksum
	#struct -- Interpret strings as packed binary data
	myChecksum = 0
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	data = struct.pack("d", time.time())
	#Calculates the checksum on the data and the dummy header
	#Get the right checksum, and put in the header
	myChecksum = checksum(header + data)
	if sys.platform == 'darwin':
		myChecksum = socket.htons(myChecksum) & 0xffff
	else:
		myChecksum = socket.htons(myChecksum)
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	packet = header + data
	#AF_INET address must be tuple, not str
	clientSocket.sendto(packet, (destAddr, 1))

def doOnePing(destAddr, timeout):
	icmp = socket.getprotobyname("icmp")
	#Fill in start
	#Create socket here
	#Tries to create socket 'clientSocket' for connection
	try:
		#In my testing, it always fails to create 'clientSocket', and as a result goes to the exception case
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
	except socket.error, (errno, msg):
		#Displays the error message that this action is not permitted, you cannot access the socket
		raise socket.error(msg)
	#Fill in end
	myID = os.getpid() & 0xFFFF
	sendOnePing(clientSocket, destAddr, myID)
	delay = receiveOnePing(clientSocket, myID, timeout, destAddr)
	
	clientSocket.close()
	return delay

def ping(host, timeout = 1):
	dest = socket.gethostbyname(host)
	print "Pinging " + dest + " using Python:"
	print ""
	
	#Send ping requests to a server separated by approximately one second
	while 1:
		delay = doOnePing(dest, timeout)
		print doOnePing(dest, timeout)
		time.sleep(1)
		return delay

#Other websites I tried to ping, but had little success in doing
#ping("www.poly.edu")
#ping("www.csus.edu")
ping("www.google.com")