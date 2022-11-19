import  socket

class BluetoothServerSocket(object):
	def __init__(self, port):
		self.MAC = '08:BE:AC:0F:2F:E1' # MAC of the Jetson Nano 
		self.port = port # Lower ports appear to be occupied
		self.bufferSize = 1024
		self.backlog = 1
		self.socket = None
		self.client = None
		self.clientAddress = None

	# Must call before using the bluetooth socket, sets the socket, client socket, and client socket address
	def initServerSocket(self):
		self.socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
		self.socket.bind((self.MAC,self.port))
		self.socket.listen(self.backlog)
		try:
			self.client, self.clientAddress = self.socket.accept()
		except:
			print("Unable to establish bluetooth socket connection")
			self.client.close()
			self.socket.close()

	def send(self, message):
		self.client.send(bytes(message, 'UTF-8'))

	# Return the received data as a string
	def receive(self):
		while 1:
			data = self.client.recv(self.bufferSize)
			if data:
				return data.decode('UTF-8')

	def close(self):
		self.client.close()
		self.socket.close()