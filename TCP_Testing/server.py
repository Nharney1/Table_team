import socket, struct
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostIP = socket.gethostbyname(socket.gethostname())
while 1:
	s.bind((hostIP, 50000))
	s.listen(3)
	while 1:
		try:
			conn, addr = s.accept()
			while 1:
				data = conn.recv(1024).decode()
				if not data:
					continue
				print(data)
				conn.sendall('Message recieved'.encode('utf-8'))
		except(OSError) as e:
			conn.close()
