import socket

class videosocket:
	"""
		A special type socket to handle the sending and receiving of fixed
		size frame strings over usual sockets.
		Size of packet is assumed to be less than 100MB.
	"""
	
	def __init__(self, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock
	
	def connect(self, host, port):
		self.sock.connect(host,port)
	
	def vsend(self, framestring):
		totalsent = 0
		metasent = 0
		length = len(framestring)
		lengthstr = str(length).zfill(8)
		
		while metasent < 8:
			sent = self.sock.send(lengthstr[metasent:])
			if sent == 0:
				raise RuntimeError("Socket connection broken")
			metasent += sent
		
		while totalsent < length:
			sent = self.sock.send(framestring[totalsent:])
			if sent == 0:
				raise RuntimeError("Socket connection broken")
			totalsent += sent
		
	def vreceive(self):
		totalrec = 0
		metarec = 0
		msgArray = []
		metaArray = []
		
		while metarec < 8:
			chunck = self.sock.recv(8 - metarec)
			if chunck == '':
				raise RuntimeError("Socket connection broken")
			metaArray.append(chunck)
			metarec += len(chunck)
			
		lengthstr = ''.join(metaArray)
		length = int(lengthstr)
		
		while totalrec < length :
			chunck = self.sock.recv(length - totalrec)
			if chunck == '':
				raise RuntimeError("Socket connection broken")
			msgArray.append(chunck)
			totalrec += len(chunck)
		
		return ''.join(msgArray)