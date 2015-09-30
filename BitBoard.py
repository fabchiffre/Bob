from bitarray import bitarray

WHITE = 1
BLACK = -1

PAWN = 'p'
QUEEN = 'q'
KNIGHT = 'n'

class Move(object):
    def __init__(self, piece_type, pos_init, pos_final, board):
       self.piece_type = piece_type
       self.pos_init = pos_init
       self.pos_final = pos_final

    def apply(self):
    	pass

    def undo(self):
    	pass


class BitBoard(object):
	def __init__(self, state):
		self.pieces = {}

		self.pieces[WHITE] = {} 
		self.pieces[BLACK] = {}

		self.pieces[WHITE][PAWN] = bitarray(64)
		self.pieces[WHITE][PAWN].setall(0)

		self.pieces[WHITE][QUEEN] = bitarray(64)
		self.pieces[WHITE][QUEEN].setall(0)
		
		self.pieces[WHITE][KNIGHT] = bitarray(64)
		self.pieces[WHITE][KNIGHT].setall(0)

		self.pieces[BLACK][PAWN] = bitarray(64)
		self.pieces[BLACK][PAWN].setall(0)
		
		self.pieces[BLACK][QUEEN] = bitarray(64)
		self.pieces[BLACK][QUEEN].setall(0)

		self.pieces[BLACK][KNIGHT] = bitarray(64)
		self.pieces[BLACK][KNIGHT].setall(0)
		
		c = state['board']
		print c
		i=0
		print "Reads from state"
		for row in xrange(7, -1, -1):
			for col in xrange(0, 8):
				print c[i]
				if c[i] != '.':
					team = BLACK if c[i].lower() == c[i] else WHITE
					self.pieces[team][c[i].lower()][row*8 + col] = 1
				i += 1

	def count_pop_bit_board(self, bb):
		count = 0
		while(bb):
			count += 1
			bb &= bb - 1
		return count

	def generate(self):
		pass

	def print_bitboard(self, bb):
		for i in range(7, -1, -1):
			for j in range(0, 8):
				print(bb[i*8 + j]),
			print "\n"

