import copy
from bitarray import bitarray

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
row7File = bitarray('1111111100000000000000000000000000000000000000000000000000000000')

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
	def __init__(self, team, piece_type, pos_init, pos_final):
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


	def apply(self, board):
		new_board = copy.deepcopy(board)
		new_board.pieces[self.team][self.piece_type] ^= self.from_to
		if((new_board.pieces[-self.team][PAWN] & self.pos_final_bb).any()):
			new_board.pieces[-self.team][PAWN] ^= self.pos_final_bb
		if((new_board.pieces[-self.team][KNIGHT] & self.pos_final_bb).any()):
			new_board.pieces[-self.team][KNIGHT] ^= self.pos_final_bb
		if((new_board.pieces[-self.team][QUEEN] & self.pos_final_bb).any()):
			new_board.pieces[-self.team][QUEEN] ^= self.pos_final_bb
		return new_board

class BitBoard(object):
	def __init__(self, state, my_team):
		self.my_team = my_team
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

		self.team = state.team

		c = state['board']
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

	def _check_move(self, team, type_p, pos_init, bb_final, adv, moves):
		if bb_final.any():
			pos_final = bb_final.index(1)
			if (adv & bb_final).any():
				moves.insert(0, Move(team, type_p, (pos_init/8, pos_init%8), (pos_final/8, pos_final%8)))
			else:
				moves.append(Move(team, type_p, (pos_init/8, pos_init%8), (pos_final/8, pos_final%8)))

	def heuristic(self):
		# check winners
		if self.wins(self.my_team):
			return float('inf')
		if self.wins(-self.my_team):
			return float('-inf')

		# compute value
		res = 0
		# diff of pieces value
		res += (self.countKnight(self.my_team) - self.countKnight(-self.my_team)) * valPoint[KNIGHT]
		res += (self.countQueen(self.my_team) - self.countQueen(-self.my_team)) * valPoint[QUEEN]
		res += (self.countPawn(self.my_team) - self.countPawn(-self.my_team)) * valPoint[PAWN]
		# diff of advancment of pawns
		res += (self.distPawn(self.my_team) - distPawn(-self.my_team))

		return res

	def wins(self, team):
		# no pawn on our side = LOSE
		pieces = self.pieces[team][PAWN]
		if pieces == 0:
			return False
		# no pawn on other side = WIN
		otherPieces = self.pieces[-team][PAWN]
		if otherPieces == 0:
			return True
		# pawn on last line
		mask = row0File
		if team == WHITE:
			mask = row7File
		lastLinePawn = self.pieces[team][PAWN] & mask
		return (lastLinePawn != 0)

	def countQueen(self, team):
		if (self.pieces[team][QUEEN].any()):
			return 1

	def countPawn(self, team):
		res = 0
		mask = 1
		for x in xrange(0,63):
			if (self.pieces[team][PAWN] & mask) != 0:
				res += 1
			mask <<= 1

	def countKnight(self, team):
		res = 0
		mask = 1
		for x in xrange(0,63):
			if (self.pieces[team][KNIGHT] & mask) != 0:
				res += 1
			mask <<= 1

	def distPawn(self, team):
		res = 0
		mask = 1
		for x in xrange(0,63):
			if (self.pieces[team][PAWN] & mask) != 0:
				if team == WHITE:
					dist = (int) (x/8 - 1)
					res += dist*dist
				if team == BLACK:
					dist = (int) (6 - x/8)
					res += dist*dist
			mask <<= 1

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
		# self._generate_pawn(team, adv, empty, moves)
		# self._generate_knight(team, adv, empty, moves)
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

			self._check_move(team, PAWN, pos_init, bb_final, adv, moves)

			# Normal capture
			if team == WHITE:
				bb_final_1 = rightshift(bb_init, 7) & adv & notHFile
				bb_final_2 = rightshift(bb_init, 9) & adv & notAFile
			else:
				bb_final_1 = leftshift(bb_init, 7) & adv & notHFile
				bb_final_2 = leftshift(bb_init, 9) & adv & notAFile

			self._check_move(team, PAWN, pos_init, bb_final_1, adv, moves)
			self._check_move(team, PAWN, pos_init, bb_final_2, adv, moves)

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
			self._check_move(team, KNIGHT, pos_init, bb_final, adv, moves)

			bb_final = rightshift(bb_init, 10) & notABFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, adv, moves)

			bb_final = leftshift(bb_init, 6) & notABFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, adv, moves)

			bb_final = leftshift(bb_init, 15) & notAFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, adv, moves)

			bb_final = rightshift(bb_init, 15) & notHFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, adv, moves)

			bb_final = rightshift(bb_init, 6) & notGHFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, adv, moves)

			bb_final = leftshift(bb_init, 10) & notGHFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, adv, moves)


			bb_final = leftshift(bb_init, 17) & notHFile & (empty | adv)
			self._check_move(team, KNIGHT, pos_init, bb_final, adv, moves)


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
				self._check_move(team, QUEEN, pos_init, bb_final, adv, moves)
			elif adv[pos_init-i]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init -i] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, adv, moves)
				break
			else:
				break

		# Generate right
		for i in range(1, 8 - pos_init_x):
			if empty[pos_init+i]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init + i] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, adv, moves)
			elif adv[pos_init+i]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init + i] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, adv, moves)
				break
			else:
				break

		# Generate bottom
		for i in range(1, pos_init_y + 1):
			if empty[pos_init - i * 8 ]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init - i * 8] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, adv, moves)
			elif adv[pos_init - i * 8]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init - i * 8] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, adv, moves)
				break
			else:
				break

		# Generate top
		for i in range(1, 8 - pos_init_y):
			if empty[pos_init + i * 8]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init + i * 8] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, adv, moves)
			elif adv[pos_init + i * 8]:
				bb_final = bitarray(64)
				bb_final.setall(0)
				bb_final[pos_init + i * 8] = 1
				self._check_move(team, QUEEN, pos_init, bb_final, adv, moves)
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
				self._check_move(team, QUEEN, pos_init, bb_final, adv, moves)
				if adv[q_row * 8 + q_col]:
					break
			else:
				break


