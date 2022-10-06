import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50000))
while 1:
	str = input("What would you like to send?\n")
	if str != '':
		s.sendall(str.encode('utf-8'))
		data = s.recv(1024)
