from BitBoard import *
import time
from collections import deque

alpha = float('inf')
beta = float('-inf')

class MoveTree(object):
	"""base to create a movement tree"""
	def __init__(self, bitboard, move=None, isMin=False, depth=0):
		if move != None:
			self.move = move
		self.isMin = isMin
		self.bitboard = bitboard
		self.children = []
		self.depth = depth

	def build_children_withdepth(self, depth=0):
		if depth > 0:
			if self.isMin:
				nextMoves = self.bitboard.generate(-self.bitboard.my_team)
			else:
				nextMoves = self.bitboard.generate(self.bitboard.my_team)
			for m in nextMoves:
				node = MoveTree(m.apply(self.bitboard), m, not self.isMin, depth-1)
				node.build_children_withdepth(depth-1)
				self.children.append(node)
		return self.children

	def build_children(self):
		if self.isMin:
			nextMoves = self.bitboard.generate(-self.bitboard.my_team)
		else:
			nextMoves = self.bitboard.generate(self.bitboard.my_team)
		for m in nextMoves:
			node = MoveTree(m.apply(self.bitboard), m, not self.isMin)
			self.children.append(node)
		return self.children

	def get_heuristic(self):
		return self.bitboard.heuristic()

	def compute_alpha_beta(self):
		global alpha
		global beta
		if not self.children:
			return self.get_heuristic()
		if self.isMin:
			v = float('inf')
			for child in self.children:
				v = min(v, child.compute_alpha_beta())
				alpha = min(alpha, v)
				if alpha >= beta:
					break
			return v

		else:
			v = float('-inf')
			for child in self.children:
				v = max(v, child.compute_alpha_beta())
				beta = max(beta, v)
				if alpha >= beta:
					break
			return v

	def compute_alpha_beta_incr(self, prev_score):
		global alpha
		global beta
		delta = self.move.compute_delta(self.bitboard)
		score = prev_score + delta
		if not self.children:
			return score
		if self.isMin:
			v = float('inf')
			for child in self.children:
				v = min(v, child.compute_alpha_beta_incr(score))
				alpha = min(alpha, v)
				if alpha >= beta:
					break
			return v
		else:
			v = float('-inf')
			for child in self.children:
				v = max(v, child.compute_alpha_beta_incr(score))
				beta = max(beta, v)
				if alpha >= beta:
					break
			return v

	def get_best_move(self):
		global alpha
		alpha = float('inf')
		global beta
		beta = float('-inf')

		best_move = None
		for n in self.children:
			val = n.compute_alpha_beta()
			if best_move == None or best_val < val:
				best_move = n
				best_val = val

		return best_move


	def root_build_children(self, time_zero):
		t_zero = time_zero
		queue = deque()
		# look for leaves
		# breadth-first search
		nodesToExplore = deque()
		nodesToExplore.append(self)
		while len(nodesToExplore) != 0:
			node = nodesToExplore.popleft()
			if node.children == []:
				queue.append(node)
			else:
				nodesToExplore.extend(node.children)
		# build children, still BFS order
		while(time.time() < t_zero + 4.):
			node = queue.popleft()
			children = node.build_children()
			queue.extend(children)

	def get_right_child(self, bitboard):
		for child in self.children:
			if bitboard.equals(child.bitboard):
				return child
		return None
