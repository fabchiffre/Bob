import sys
import socket
import time
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
		t_zero = time.time()

		self.my_team = state['who_moves']

		print 'Generating a move...',
		board = BitBoard(state=state, my_team=self.my_team)

		self.move_tree = MoveTree(bitboard=board)

		# if (self.my_team == WHITE and int(state['white_infractions']) < 4) or (self.my_team == BLACK and int(state['black_infractions']) < 4):
		# 	best_move = self.move_tree.get_best_move_alpha_beta(5)
		# else:
		# 	best_move = self.move_tree.get_best_move_alpha_beta(4)
		best_move = self.move_tree.root_alpha_beta_max_dynamic(5, t_zero)


		self.send_move(best_move.pos_init, best_move.pos_final)

		print str(best_move.pos_init) + ", " + str(best_move.pos_final)

	def on_game_over(self, state):
		print "Game Over"
		self._socket.close()
		sys.exit()
		
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


