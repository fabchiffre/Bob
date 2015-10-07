import copy
from bitarray import *

WHITE = 1
BLACK = -1

PAWN = 'p'
QUEEN = 'q'
KNIGHT = 'n'

notAFile = bitarray('0111111101111111011111110111111101111111011111110111111101111111')
notBFile = bitarray('1011111110111111101111111011111110111111101111111011111110111111')
notGFile = bitarray('1111110111111101111111011111110111111101111111011111110111111101')
notHFile = bitarray('1111111011111110111111101111111011111110111111101111111011111110')

row0File = bitarray('0000000000000000000000000000000000000000000000000000000011111111')
row1File = bitarray('0000000000000000000000000000000000000000000000001111111100000000')
row2File = bitarray('0000000000000000000000000000000000000000111111110000000000000000')
row3File = bitarray('0000000000000000000000000000000011111111000000000000000000000000')
row4File = bitarray('0000000000000000000000001111111100000000000000000000000000000000')
row5File = bitarray('0000000000000000111111110000000000000000000000000000000000000000')
row6File = bitarray('0000000011111111000000000000000000000000000000000000000000000000')
row7File = bitarray('1111111100000000000000000000000000000000000000000000000000000000')

rowFile = [row0File, row1File, row2File, row3File, row4File, row5File, row6File, row7File]
rowValue = {}
rowValue[BLACK] = [0, 1, 2, 4, 8, 16, 32, 100000]
rowValue[WHITE] = [100000, 32, 16, 8, 4 , 2, 1, 0]

coefDistPawn = 0.2

notABFile = notAFile & notBFile
notGHFile = notGFile & notHFile

valPoint = {}
valPoint[PAWN] = 1.2
valPoint[KNIGHT] = 3.3
valPoint[QUEEN] = 8.8

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
	def __init__(self, team, piece_type, pos_init, pos_final, capture=False, capture_type=None):
		self.team = team
		self.piece_type = piece_type
		self.pos_init = pos_init
		self.pos_final = pos_final

		self.pos_init_bb = bitarray(64)
		self.pos_init_bb.setall(0)
		self.pos_init_bb[pos_init[0]*8 + pos_init[1]] = 1

		self.pos_final_bb = bitarray(64)
		self.pos_final_bb.setall(0)
		self.pos_final_bb[pos_final[0]*8 + pos_final[1]] = 1

		self.from_to = self.pos_init_bb ^ self.pos_final_bb

		self.capture = capture
		self.capture_type = capture_type


	def apply(self, board):
		new_board = copy.deepcopy(board)
		new_board.pieces[self.team][self.piece_type] ^= self.from_to
		if(self.capture):
				new_board.pieces[-self.team][capture_type] ^= self.pos_final_bb
		return new_board

class BitBoard(object):
	def __init__(self, state=None, my_team=0, bitboard=None):
		self.pieces = {}

		self.pieces[WHITE] = {}
		self.pieces[BLACK] = {}

		if bitboard == None:
			self.my_team = my_team
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
			i=0
			for row in xrange(7, -1, -1):
				for col in xrange(0, 8):
					if c[i] != '.':
						team = BLACK if c[i].lower() == c[i] else WHITE
						self.pieces[team][c[i].lower()][row*8 + col] = 1
					i += 1
		else:
			self.my_team = bitboard.my_team
			self.pieces[WHITE][PAWN] = bitarray(bitboard.pieces[WHITE][PAWN])
			self.pieces[WHITE][QUEEN] = bitarray(bitboard.pieces[WHITE][PAWN])
			self.pieces[WHITE][KNIGHT] = bitarray(bitboard.pieces[WHITE][PAWN])
			self.pieces[BLACK][PAWN] = bitarray(bitboard.pieces[WHITE][PAWN])
			self.pieces[BLACK][QUEEN] = bitarray(bitboard.pieces[WHITE][PAWN])
			self.pieces[BLACK][KNIGHT] = bitarray(bitboard.pieces[WHITE][PAWN])


	def equals(self, bitboard):
		ans = True
		ans &= ( bitdiff(self.pieces[BLACK][PAWN], bitboard.pieces[BLACK][PAWN]) == 0 )
		ans &= ( bitdiff(self.pieces[WHITE][PAWN], bitboard.pieces[WHITE][PAWN]) == 0 )
		ans &= ( bitdiff(self.pieces[BLACK][QUEEN], bitboard.pieces[BLACK][QUEEN]) == 0 )
		ans &= ( bitdiff(self.pieces[WHITE][QUEEN], bitboard.pieces[WHITE][QUEEN]) == 0 )
		ans &= ( bitdiff(self.pieces[BLACK][KNIGHT], bitboard.pieces[BLACK][KNIGHT]) == 0 )
		ans &= ( bitdiff(self.pieces[WHITE][KNIGHT], bitboard.pieces[WHITE][KNIGHT]) == 0 )
		return ans;

	def _check_move(self, team, type_p, pos_init, bb_final, moves):
		if bb_final.any():
			pos_final = bb_final.index(1)
			if (self.pieces[-self.my_team][PAWN] & bb_final).any():
				moves.insert(0, Move(team, type_p, (pos_init/8, pos_init%8), (pos_final/8, pos_final%8), True, PAWN))
			elif (self.pieces[-self.my_team][KNIGHT] & bb_final).any():
				moves.insert(0, Move(team, type_p, (pos_init/8, pos_init%8), (pos_final/8, pos_final%8), True, KNIGHT))
			elif (self.pieces[-self.my_team][QUEEN] & bb_final).any():
				moves.insert(0, Move(team, type_p, (pos_init/8, pos_init%8), (pos_final/8, pos_final%8), True, QUEEN))
			else:
				moves.append(Move(team, type_p, (pos_init/8, pos_init%8), (pos_final/8, pos_final%8), False))

	def heuristic(self):
		# check winners
		if self.wins(self.my_team):
			return float('inf')
		if self.wins(-self.my_team):
			return float('-inf')
		# compute value
		res = 0
		# diff of pieces value
		res += (self.pieces[self.my_team][KNIGHT].count() - self.pieces[-self.my_team][KNIGHT].count()) * valPoint[KNIGHT]
		res += (self.pieces[self.my_team][QUEEN].count() - self.pieces[-self.my_team][QUEEN].count())  * valPoint[QUEEN]
		res += (self.pieces[self.my_team][PAWN].count() - self.pieces[-self.my_team][PAWN].count())  * valPoint[PAWN]

		# diff of advancment of pawns
		res += ((self.distPawn(self.my_team) - self.distPawn(-self.my_team))) * coefDistPawn

		return res

	def wins(self, team):
		# no pawn on our side = LOSE
		pieces = self.pieces[team][PAWN]
		if pieces.count() == 0:
			return False
		# no pawn on other side = WIN
		otherPieces = self.pieces[-team][PAWN]
		if otherPieces.count() == 0:
			return True
		# # pawn on last line
		# mask = row0File
		# if team == WHITE:
		# 	mask = row7File
		# lastLinePawn = self.pieces[team][PAWN] & mask
		# return (lastLinePawn != 0)

	def distPawn(self, team):
		res = 0
		for x in range(0,8):
			pop = (self.pieces[team][PAWN] & rowFile[x]).count()
			res += pop * rowValue[team][x]
		return res

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
		self._generate_pawn(team, adv, empty, moves)
		self._generate_knight(team, adv, empty, moves)
		self._generate_queen(team, adv, empty, moves)

		return moves

	def _generate_pawn(self, team, adv, empty, moves):
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

			self._check_move(team, PAWN, pos_init, bb_final, moves)

			# Normal capture
			if team == WHITE:
				bb_final_1 = rightshift(bb_init, 7) & adv & notHFile
				bb_final_2 = rightshift(bb_init, 9) & adv & notAFile
			else:
				bb_final_1 = leftshift(bb_init, 7) & adv & notHFile
				bb_final_2 = leftshift(bb_init, 9) & adv & notAFile

			self._check_move(team, PAWN, pos_init, bb_final_1, moves)
			self._check_move(team, PAWN, pos_init, bb_final_2, moves)

			pawns ^= bb_init

	def _generate_knight(self, team, adv, empty, moves):
		knights =  bitarray(self.pieces[team][KNIGHT])

		''' Loop for each pawn '''
		while(knights.any()):
			pos_init = knights.index(1)

			bb_init = bitarray(64)
			bb_init.setall(0)
			bb_init[pos_init] = 1

			bb_final = rightshift(bb_init, 17) & notAFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, moves)

			bb_final = rightshift(bb_init, 10) & notABFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, moves)

			bb_final = leftshift(bb_init, 6) & notABFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, moves)

			bb_final = leftshift(bb_init, 15) & notAFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, moves)

			bb_final = rightshift(bb_init, 15) & notHFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, moves)

			bb_final = rightshift(bb_init, 6) & notGHFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, moves)

			bb_final = leftshift(bb_init, 10) & notGHFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, moves)

			bb_final = leftshift(bb_init, 17) & notHFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, moves)


			knights ^= bb_init

	def _generate_queen(self, team, adv, empty, moves):
		if self.pieces[team][QUEEN].any():
			pos_init = self.pieces[team][QUEEN].index(1)
			self._generate_rook(team, adv, empty, moves)
			self._generate_bishop(team, pos_init, empty, adv, moves, row_dir=1, col_dir=1) # TOPRIGHT
			self._generate_bishop(team, pos_init, empty, adv, moves, row_dir=1, col_dir=-1) # TOPLEFT
			self._generate_bishop(team, pos_init, empty, adv, moves, row_dir=-1, col_dir=-1) # BOTTOMLEFT
			self._generate_bishop(team, pos_init, empty, adv, moves, row_dir=-1, col_dir=1) # BOTTOMRIGHT

	def _generate_rook(self, team, adv, empty, moves):
		pos_init = self.pieces[team][QUEEN].index(1)
		pos_init_y = pos_init / 8
		pos_init_x = pos_init % 8
		# Generate left
		for i in range(1, pos_init_x + 1):
			if empty[pos_init -i ]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init - i] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, moves)
			elif adv[pos_init-i]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init -i] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, moves)
				break
			else:
				break

		# Generate right
		for i in range(1, 8 - pos_init_x):
			if empty[pos_init+i]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init + i] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, moves)
			elif adv[pos_init+i]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init + i] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, moves)
				break
			else:
				break

		# Generate bottom
		for i in range(1, pos_init_y + 1):
			if empty[pos_init - i * 8 ]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init - i * 8] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, moves)
			elif adv[pos_init - i * 8]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init - i * 8] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, moves)
				break
			else:
				break

		# Generate top
		for i in range(1, 8 - pos_init_y):
			if empty[pos_init + i * 8]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init + i * 8] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, moves)
			elif adv[pos_init + i * 8]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init + i * 8] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, moves)
				break
			else:
				break

	def _generate_bishop(self, team, pos_init, empty, adv, moves, row_dir, col_dir):
		my_row = pos_init / 8
		my_col = pos_init % 8

		for i in xrange(1, 8):
			row = row_dir*i
			col = col_dir*i
			q_row, q_col = my_row+row, my_col+col

			if not 0 <= q_row <= 7 or not 0 <= q_col <= 7:
				break

			if empty[q_row * 8 + q_col] or adv[q_row * 8 + q_col]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[q_row * 8 + q_col] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, moves)
				if adv[q_row * 8 + q_col]:
					break
			else:
				break


