from pyircfish.pyircfish import bots

#This class is required to be able to use the bot to any degree of being able to read anything being sent to it from the server. You can also use a dictionary with the same values
class IRCHandler:
	
	def __init__(self, main):
		self.main = main
	
	def onconnecting(self, server, port):
		print "Connecting to "+server+":"+port+"..."
	
	def onconnected(self, server, port):
		print "Connected to "+server+":"+port+"."
		self.main.bot.protocol.joinChannel("#TestChannel1323")
	
	def ondisconnected(self, server, port):
		print "Disconnected from "+server+":"+port+"."
	
	def onnotice(self, server, user, message):
		print "-"+user+"- "+message
		if user == "NickServ":
			if "registered and protected." in message: # NickServ wants the password for your chosen username.
				self.main.bot.protocol.nsid("yourpasswordfornickserv")
			elif "accepted - you are" in message: # Password was accepted, you are now recognized.
				print "Verified identify to NickServ."
	
	def onjoin(self, server, channel, user):
		print user+" has joined channel "+channel
	
	def onpart(self, server, channel, user):
		print user+" has left channel "+channel
	
	def onquit(self, server, user, reason):
		print user+" has quit. ("+reason+")"
	
	def onprivmsg(self, server, to, user, message, action):
		if to[0:1] == "#": # Channel Message
			if action:
				print "["+to+"]* "+user+" "+message
			else:
				# Here would be where you could use the encrypt and decrypt functions for FiSH.
				#if message[0:3] == "+OK" # Check if its encrypted text incoming.
				#	message = self.main.bot.decrypt("FiSHKeyGoesHere", message)
				print "["+to+"]<"+user+"> "+message
		else: # Privmate Message
			if action:
				print "[PRIVATE]* "+user+" "+message
			else:
				print "[PRIVATE]<"+user+"> "+message

class testbot:
	
	def __init__(self):
		self.quit = False
		self.botlist = None
		self.bot = None
	
	def privmsg(self, to, message, action=False):
		# You would need a wrapper function like so to enable sending out encrypted FiSH text. I've included a general example of how to commented out.
		#if to[0:1] == "#" and message[0:3] == "+OK" # Check if its encrypted text incoming and is a channel.
		#	message = self.main.bot.encrypt("FiSHKeyGoesHere", message)
		self.bot.protocol.privmsg(self, to, message, action)

	def main(self):
		self.botlist = bots() # Create new instance of the bots class.
		# The following line creates the bot and performs the connect command as well, any variables with their names defined are optional and can be put in any order as long as the names are given. 
		# The order they are in here is the default order.
		self.bot = self.botlist.makebot("irc.efnet.org", 6667, "pyIRCFiSH", realname="pyIRCFiSH", ssl=False, events=IRCHandler(self), verbose=False)
		# Note the bots will run in their own threads and will not block the program, so a while loop is needed to keep the program running.
		while not testbot.quit:
			command = raw_input()
			if command == "quit":
				testbot.quit = True
		testbot.bot.protocol.quit("Dead")
		testbot.bot.disconnect()

if __name__ == "__main__":
	testbot = testbot()
	testbot.main()