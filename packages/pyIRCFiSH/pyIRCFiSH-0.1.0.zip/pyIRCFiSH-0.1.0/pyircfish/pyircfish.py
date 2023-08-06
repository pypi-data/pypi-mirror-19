from protocol import protocol, handler
import socket, time, ssl, irccrypt, threading

class bots:
	
	def __init__(self):
		self.bots = []
	
	def addbot(self, check):
		if isinstance(check, bot):
			self.bots.append(check)
	
	def delbot(self, check):
		if isinstance(check, bot):
			self.bots.remove(check)
	
	def getbotbyserver(self, server):
		for check in self.bots:
			if check.server == server:
				return check
		return False
	
	def makebot(self, server, port, username, realname="", ssl=False, events=None, verbose=False):
		newbot = bot(server, port, username, realname, ssl, events, verbose)
		newbot.connect()
		self.addbot(newbot)
		return newbot

class bot:
	def __init__ (self, server, port, username, realname="", ssl=False, events=None, verbose=False):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = server
		self.port = port
		self.username = username
		self.realname = realname
		self.ssl = ssl
		self.verbose = verbose
		self.quit = False
		self.events = events
		self.protocol = protocol(self)
		self.handler = handler(self)
	
	def decrypt(self, key, inp):
		decrypt_clz = irccrypt.Blowfish
		decrypt_func = irccrypt.blowcrypt_unpack
		if 3 <= inp.find(' *') <= 4:
			decrypt_clz = irccrypt.BlowfishCBC
			decrypt_func = irccrypt.mircryption_cbc_unpack
		b = decrypt_clz(key)
		return decrypt_func(inp, b)

	def encrypt(self, key, inp):
		b = irccrypt.Blowfish(key)
		return irccrypt.blowcrypt_pack(inp, b)
	
	def log(self, message):
		if not self.verbose:
			print "[IRC]"+message
	
	def sendData(self, data):
		if self.verbose:
			print "OUT: " + data.strip()
		if self.s and data != "":
			self.s.send(data)
	
	def disconnect(self):
		self.s.close()
		self.sckthrd.join()
		self.s = None
		self.sckthrd = None

	def connect(self):
		if isinstance(self.events, dict):
			if 'onconnecting' in self.events:
				self.events['onconnecting'](self.server, str(self.port))
		else:
			if 'onconnecting' in dir(self.events):
				self.events.onconnecting(self.server, str(self.port))
		self.s.connect((self.server, self.port))
		if self.ssl:
			self.s = ssl.wrap_socket(self.s)
		self.protocol.sendNickUser()
		self.sckthrd = threading.Thread(target=self.recv)
		self.sckthrd.daemon = True
		self.sckthrd.start()
	
	def recv(self):
		while True:
			data = self.s.recv(4096)
			n = data.split("\r\n")
			for command in n:
				if command != "":
					if self.verbose:
						print "IN: " + command.strip()
					self.handler.process(command.strip())
	