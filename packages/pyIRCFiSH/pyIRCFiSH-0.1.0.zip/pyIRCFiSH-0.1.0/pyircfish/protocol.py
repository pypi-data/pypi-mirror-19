import re

class protocol:
	
	def __init__(self, bot):
		self.bot = bot

	def sendNickUser(self):
		self.bot.sendData("NICK "+self.bot.username+"\r\n")
		self.bot.sendData("USER "+self.bot.username+" 0 * :"+self.bot.realname+"\r\n")
	
	def joinChannel(self, channel, joinmessage=""):
		self.bot.sendData("JOIN "+channel+"\r\n")
		if joinmessage != "":
			self.bot.sendData("PRIVMSG "+channel+" :"+joinmessage+"\r\n")
	
	def leaveChannel(self, channel, reason=""):
		self.bot.sendData("PART "+channel+" :"+reason+"\r\n")
	
	def quit(self, reason=""):
		self.bot.sendData("QUIT :"+reason+"\r\n")
	
	def privmsg(self, to, message, action=False):
		if action:
			self.bot.sendData("PRIVMSG "+to+" :\x01ACTION "+message+"\x01\r\n")
		else:
			self.bot.sendData("PRIVMSG "+to+" :"+message+"\r\n")
		
	def nsreg(self, password, email):
		self.privmsg("NickServ", "REGISTER "+password+" "+email)
	
	def nsid(self, password):
		self.privmsg("NickServ", "IDENTIFY "+password)
	
	def pong(self, message):
		self.bot.sendData("PONG :"+message+"\r\n")

class handler:

	def __init__(self, bot):
		self.bot = bot
	
	def proc_notice(self, data):
		t = data.split(":", 2)
		line = t[1]
		f = line.split(" ", 2)
		user = f[0]
		if "!" in user:
			user = user[0:user.find("!")]
		to = f[2].strip()
		if len(t) == 3:
			message = t[2]
		else:
			message = ""
		if isinstance(self.bot.events, dict):
			if 'onnotice' in self.bot.events:
				self.bot.events['onnotice'](self.bot.server, user, message)
		else:
			if "onnotice" in dir(self.bot.events):
				self.bot.events.onnotice(self.bot.server, user, message)
	
	def proc_join(self, data):
		t = data.split(" ", 3)
		user = t[0][1:]
		if "!" in user:
			user = user[0:user.find("!")]
		command = t[1]
		channel = t[2][1:]
		if isinstance(self.bot.events, dict):
			if 'onjoin' in self.bot.events:
				self.bot.events['onjoin'](self.bot.server, channel, user)
		else:
			if "onjoin" in dir(self.bot.events):
				self.bot.events.onjoin(self.bot.server, channel, user)
	
	def proc_part(self, data):
		t = data.split(":", 2)
		line = t[1]
		f = line.split(" ", 2)
		user = f[0]
		if "!" in user:
			user = user[0:user.find("!")]
		to = f[2].strip()
		if len(t) > 2: #Reason
			message = t[2]
		else:
			message = ""
		if isinstance(self.bot.events, dict):
			if 'onpart' in self.bot.events:
				self.bot.events['onpart'](self.bot.server, channel, user, message)
		else:
			if "onpart" in dir(self.bot.events):
				self.bot.events.onpart(self.bot.server, channel, user, message)
	
	def proc_quit(self, data):
		t = data.split(" ", 3)
		user = t[0][1:]
		if user == self.bot.username:
			self.bot.quit = True
			return
		if "!" in user:
			user = user[0:user.find("!")]
		command = t[1]
		reason = " ("+t[2][1:]+")"
		if isinstance(self.bot.events, dict):
			if 'onquit' in self.bot.events:
				self.bot.events['onquit'](self.bot.server, user, reason)
		else:
			if "onquit" in dir(self.bot.events):
				self.bot.events.onquit(self.bot.server, user, reason)
	
	def proc_privmsg(self, data):
		t = data.split(":", 2)
		line = t[1]
		f = line.split(" ", 2)
		user = f[0]
		if "!" in user:
			user = user[0:user.find("!")]
		to = f[2].strip()
		message = t[2]
		action = False
		if "\x01" in message:
			#Is Action
			action = True
			message = message[7:len(message)-1].strip()
		if isinstance(self.bot.events, dict):
			if 'onprivmsg' in self.bot.events:
				self.bot.events['onprivmsg'](self.bot.server, to, user, message, action)
		else:
			if "onprivmsg" in dir(self.bot.events):
				self.bot.events.onprivmsg(self.bot.server, to, user, message, action)

	def proc_ping(self, data):
		t = data.split(" ")
		command = t[0]
		if command.find("PING") or command.find("ING"):
			message = t[1][1:]
			self.bot.protocol.pong(message)
		else:
			return

	def proc_376(self, data):
		if " " in data:
			t = data.split(" ")
			command = t[1]
			if command == "376":
				if isinstance(self.bot.events, dict):
					if 'onconnected' in self.bot.events:
						self.bot.events['onconnected'](self.bot.server, str(self.bot.port))
				else:
					if "onconnected" in dir(self.bot.events):
						self.bot.events.onconnected(self.bot.server, str(self.bot.port))
	
	def process(self, data):
		if "NOTICE" in data:
			self.proc_notice(data)
		elif "JOIN" in data:
			self.proc_join(data)
		elif "PART" in data:
			self.proc_part(data)
		elif "QUIT" in data:
			self.proc_quit(data)
		elif "PRIVMSG" in data:
			self.proc_privmsg(data)
		elif "ING" in data:
			self.proc_ping(data)
		else:
			self.proc_376(data)