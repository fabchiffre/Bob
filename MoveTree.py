import global

class MoveTree(object):
	"""base to create a movement tree"""
	def __init__(self, move, bitboard, isMin):
		super(MoveTree, self).__init__()
		self.move = move
		self.bitboard = move.apply(bitboard)
		self.isMin = isMin
		self.children = []

	def buildChildren():
		nextMoves = self.bitboard.generateMoves()
		for m in nextMoves:
			self.children.append(new MoveTree(m, self.bitboard, !self.isMin))
		return self.children

	def score():
		return self.bitboard.computeHeuristic()

	def computeAlphaBeta():
		global alpha
		global beta
		if children.empty():
			return this.score()
		if self.isMin:
			val = float("inf")
			for child in children:
				val = min(val, child.computeAlphaBeta())
				if val < alpha:
					return val
				alpha = max(alpha, val)
		else:
			val = float("-inf")
			for child in children:
				val = max(val, child.computeAlphaBeta())
				if val > beta:
					return val
				beta = max(beta, val)
		return val
