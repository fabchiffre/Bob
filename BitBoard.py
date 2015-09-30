import copy
from bitarray import bitarray

WHITE = 1
BLACK = -1

PAWN = 'p'
QUEEN = 'q'
KNIGHT = 'n'

notAFile = bitarray('0111111101111111011111110111111101111111011111110111111101111111')
notHFile = bitarray('1111111011111110111111101111111011111110111111101111111011111110')

def print_bitboard(bb):
		for i in range(7, -1, -1):
			for j in range(0, 8):
				print(bb[i*8 + j]),
			print "\n"

def leftshift(ba, count):
    return ba[count:] + (bitarray('0') * count)

def rightshift(ba, count):
    return (bitarray('0') * count) + ba[:-count]

class Move(object):
    def __init__(self, piece_type, pos_init, pos_final):
       self.piece_type = piece_type

       self.pos_init = bitarray(64)
       self.pos_init.setall(0)
       self.pos_init[pos_init[0] + pos_init[1]*8] = 1


       self.pos_final = bitarray(64)
       self.pos_final.setall(0)
       self.pos_final[pos_final[0] + pos_final[1]*8] = 1

       self.from_to = self.pos_init ^ self.pos_final


    def apply(self, board, team):
    	new_board = copy.deepcopy(board)
    	new_board.pieces[team][self.piece_type] ^= self.from_to
    	if((new_board.pieces[-team][PAWN] & self.pos_final).any()):
    		new_board.pieces[-team][PAWN] ^= self.pos_final

    	if((new_board.pieces[-team][KNIGHT] & self.pos_final).any()):
    		new_board.pieces[-team][KNIGHT] ^= self.pos_final

    	if((new_board.pieces[-team][QUEEN] & self.pos_final).any()):
    		new_board.pieces[-team][QUEEN] ^= self.pos_final
    	return new_board

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
		for row in xrange(7, -1, -1):
			for col in xrange(0, 8):
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

	def generate_pawn(self, team, adv, empty):
		moves = []
		pawns =  bitarray(self.pieces[team][PAWN])
		''' Loop for each pawn '''
		while(pawns.any()):

			pos_init = pawns.index(1)
			bb_init = bitarray(64)
			bb_init.setall(0)
			bb_init[pos_init] = 1

			# Movement to 1 forward
			if team == WHITE:		
				bb_final = rightshift(bb_init, 8) & empty
			else:
				bb_final = leftshift(bb_init, 8) & empty
			
			if bb_final.any():
				pos_final = bb_final.index(1)
				moves.append(Move(PAWN, (pos_init%8, pos_init/8), (pos_final%8, pos_final/8)))
			# Normal capture
			if team == WHITE:
				bb_final_1 = rightshift(bb_init, 7) & adv & notHFile
				bb_final_2 = rightshift(bb_init, 9) & adv & notAFile
			else:
				bb_final_1 = leftshift(bb_init, 7) & adv & notHFile
				bb_final_2 = leftshift(bb_init, 9) & adv & notAFile

			if bb_final_1.any() :
				pos_final = bb_final_1.index(1)
				moves.append(Move(PAWN, (pos_init%8, pos_init/8), (pos_final%8, pos_final/8)))

			if bb_final_2.any() :
				pos_final = bb_final_2.index(1)
				moves.append(Move(PAWN, (pos_init%8, pos_init/8), (pos_final%8, pos_final/8)))
		
			pawns ^= bb_init
		return moves

	def generate(self, team):
		adv = bitarray(64)
		adv.setall(0)
		adv |= self.pieces[-team][PAWN]
		adv |= self.pieces[-team][QUEEN]
		adv |= self.pieces[-team][KNIGHT]

		empty = bitarray(64)
		empty.setall(0)
		empty |= adv
		empty |= self.pieces[team][PAWN]
		empty |= self.pieces[team][QUEEN]
		empty |= self.pieces[team][KNIGHT]
		empty = ~empty
		
		moves = []
		moves.extend(self.generate_pawn(team, adv, empty))

		return moves

	def _generate_knight(self, team, adv, empty):
		pass
