import sys
import socket
from MiniMax import *
from base_client import LiacBot
from BitBoard import *
from MoveTree import *

class BobClient(LiacBot):

	def __init__(self, my_team, addr_server, port_server):
		self.name= 'Bob'
		if my_team == 'white':
			self.my_team = 1
		else :
			self.my_team = -1
		self.ip = addr_server
		self.port = int(port_server)
		self.move_tree = None
		super(BobClient, self).__init__()


	def on_move(self, state):
		print 'Generating a move...',
		board = BitBoard(state=state, my_team=self.my_team)
		if self.move_tree == None:
			''' Construct the first instance '''
			self.move_tree = MoveTree(bitboard=board)
		else:
			self.move_tree = self.move_tree.get_right_child(bitboard=board)

		self.move_tree.root_build_children()
		self.move_tree = self.move_tree.get_best_move()
		self.send_move(self.move_tree.move.pos_init, self.move_tree.move.pos_final)

		''' Temporarly '''
		# print str(self.move_tree.move.pos_init) + ", " + str(self.move_tree.move.pos_final)
		# self.move_tree = None

	def on_game_over(self, state):
		self.move_tree = None

	def start(self):
		print "Bob is connecting to " + self.ip + ":" + str(self.port)
		super(BobClient, self).start()





def print_help():
	print "Bob : Beats the others bots"
	print "Bob is a bot developed for Liac Chess"
	print "Command line :"
	print "	python Bob.py [player] [ip server] [port client]"
	print "	player : black or white"

if(len(sys.argv) != 4):
	print_help()
else:
	bot = BobClient(sys.argv[1], sys.argv[2], sys.argv[3])
	bot.start()


