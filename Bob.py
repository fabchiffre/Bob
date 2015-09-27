import sys
import socket
from base_client import LiacBot
from board import *

class BobClient(LiacBot):

	def __init__(self, numClient, addrServer, portServer):
		self.name= 'Bob'
		self.numClient = numClient
		self.ip = addrServer
		self.port = portServer
	

	def on_move(self, state):
		print 'Generating a move...'
		board = Board(state)

	def on_game_over(self, state):
		pass

	def start(self):
		print "Bob is connecting to " + self.ip + ":" + self.port
		super(self.__class__, self).start



def print_help():
	print "Bob : Beats the others bots"
	print "Bob is a bot developed for Liac Chess"
	print "Command line :"
	print "	python Bob.py [player] [ip server] [port client]"
	print "	player : -1 for black or 1 for white"

if(len(sys.argv) != 4):
	print_help()
else:
	bot = BobClient(sys.argv[1], sys.argv[2], sys.argv[3])
	bot.start()
	

