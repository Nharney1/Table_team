import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.32.230.86', 50000))
while 1:
	str = input("What would you like to send?\n")
	if str != '':
		if str == 'close connection':
			s.sendall('Client closing connection'.encode('utf-8'))
			s.close()
			sys.exit()
		else:
			s.sendall(str.encode('utf-8'))
			resp = s.recv(1024)
			print(resp.decode())
