from BitBoard import *

alpha = float('-inf')
beta = float('inf')

class MoveTree(object):
	"""base to create a movement tree"""
	def __init__(self, bitboard, move=None, isMin=False, depth=0):
		if move != None:
			self.move = move
		self.isMin = isMin
		self.bitboard = bitboard
		self.children = []
		if depth > 0:
			self.build_children(depth)

	def build_children(self, depth):
		if self.isMin:
			nextMoves = self.bitboard.generate(-self.bitboard.my_team)
		else:
			nextMoves = self.bitboard.generate(self.bitboard.my_team)
		for m in nextMoves:
			node = MoveTree(m.apply(self.bitboard), m, not self.isMin, depth-1)
			self.children.append(node)
		return self.children


	def score(self):
		return self.bitboard.heuristic()

	def compute_alpha_beta(self):
		global alpha
		global beta
		if not self.children:
			return self.score()
		if self.isMin:
			val = float("inf")
			for child in self.children:
				val = min(val, child.compute_alpha_beta())
				if val < alpha:
					return val
				alpha = max(alpha, val)
		else:
			val = float("-inf")
			for child in self.children:
				val = max(val, child.compute_alpha_beta())
				if val > beta:
					return val
				beta = max(beta, val)
		return val

	def get_best_move(self):
		global alpha
		alpha = float('-inf')
		global beta
		beta = float('inf')

		best_move = None
		best_val = None
		for n in self.children:
			val = n.compute_alpha_beta()
			if best_move == None or best_val < val:
				best_move = n
				best_val = val
		return best_move
