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

	# def build_children_withdepth(self, depth=0):
	# 	if depth > 0:
	# 		if self.isMin:
	# 			nextMoves = self.bitboard.generate(-self.bitboard.my_team)
	# 		else:
	# 			nextMoves = self.bitboard.generate(self.bitboard.my_team)
	# 		for m in nextMoves:
	# 			node = MoveTree(m.apply(self.bitboard), m, not self.isMin, depth-1)
	# 			node.build_children_withdepth(depth-1)
	# 			self.children.append(node)

	def alpha_beta_max_dynamic(self, alpha, beta, depth):
		if depth == 0:
			return self.get_heuristic()

		nextMoves = self.bitboard.generate(self.bitboard.my_team)

		if len(nextMoves) == 0:
			return 0

		for m in nextMoves:
			node = MoveTree(m.apply(self.bitboard), m, True)
			if node.bitboard.winning():
				return 100000 * depth

			score = node.alpha_beta_min_dynamic(alpha, beta, depth-1)

			if score >= beta:
				return beta

			if score > alpha:
				alpha = score

		return alpha

	def root_alpha_beta_max_dynamic(self, depth, time_zero):
		alpha = float('-inf')
		beta = float('inf')
		best_move = None
		nextMoves = self.bitboard.generate(self.bitboard.my_team)

		for m in nextMoves:
			node = MoveTree(m.apply(self.bitboard), m, True)
			if node.bitboard.winning():
				best_move = m
				return best_move

			score = node.alpha_beta_min_dynamic(alpha, beta, depth-1)

			if score > alpha:
				best_move = m
				alpha = score

			if time.time() > time_zero + 4.8:
				return best_move

		return best_move

	def alpha_beta_min_dynamic(self, alpha, beta, depth):
		if depth == 0:
			return self.get_heuristic()

		nextMoves = self.bitboard.generate(-self.bitboard.my_team)
		if len(nextMoves) == 0:
			return 0

		for m in nextMoves:
			node = MoveTree(m.apply(self.bitboard), m, False)
			if node.bitboard.losing():
				return -100000 * depth

			score = node.alpha_beta_max_dynamic(alpha, beta, depth-1)

			if score <= alpha:
				return alpha

			if score < beta:
				beta = score

		return beta


	# def build_children(self):
	# 	if self.isMin:
	# 		nextMoves = self.bitboard.generate(-self.bitboard.my_team)
	# 	else:
	# 		nextMoves = self.bitboard.generate(self.bitboard.my_team)
	# 	for m in nextMoves:
	# 		node = MoveTree(m.apply(self.bitboard), m, not self.isMin)
	# 		self.children.append(node)
	# 	return self.children

	def get_heuristic(self):
		return self.bitboard.heuristic()

	# def compute_alpha_beta(self):
	# 	global alpha
	# 	global beta
	# 	if not self.children:
	# 		return self.get_heuristic()
	# 	if self.isMin:
	# 		v = float('inf')
	# 		for child in self.children:
	# 			v = min(v, child.compute_alpha_beta())
	# 			if alpha >= v:
	# 				return v
	# 			beta = min(beta, v)
	# 		return v

	# 	else:
	# 		v = float('-inf')
	# 		for child in self.children:
	# 			v = max(v, child.compute_alpha_beta())
	# 			if v >= beta:
	# 				return v
	# 			alpha = max(alpha, v)
	# 		return v

	#### Not used in this version ####
	
	# def compute_alpha_beta_incr(self, prev_score):
	# 	global alpha
	# 	global beta
	# 	delta = self.move.compute_delta(self.bitboard)
	# 	score = prev_score + delta
	# 	if not self.children:
	# 		return score
	# 	if self.isMin:
	# 		v = float('inf')
	# 		for child in self.children:
	# 			v = min(v, child.compute_alpha_beta_incr(score))
	# 			alpha = min(alpha, v)
	# 			if alpha >= beta:
	# 				break
	# 		return v
	# 	else:
	# 		v = float('-inf')
	# 		for child in self.children:
	# 			v = max(v, child.compute_alpha_beta_incr(score))
	# 			beta = max(beta, v)
	# 			if alpha >= beta:
	# 				break
	# 		return v

	def get_best_move_alpha_beta(self, depth, time_zero):
		self.alpha_beta_max_dynamic(float('-inf'), float('inf'), depth, time_zero)
		return self.best_move


	# def get_best_move(self):
	# 	global alpha
	# 	alpha = float('-inf')
	# 	global beta
	# 	beta = float('inf')

	# 	best_move = None
	# 	for n in self.children:
	# 		val = n.compute_alpha_beta()
	# 		print "Movement : " + str(n.move.pos_init) + " to " + str(n.move.pos_final) + " value :" + str(val)

	# 		if best_move == None or best_val < val:
	# 			best_move = n
	# 			best_val = val

	# 	return best_move

	#### Not used in this version ####

	# def root_build_children(self, time_zero):
	# 	t_zero = time_zero
	# 	queue = deque()
	# 	# look for leaves
	# 	# breadth-first search
	# 	nodesToExplore = deque()
	# 	nodesToExplore.append(self)
	# 	while len(nodesToExplore) != 0:
	# 		node = nodesToExplore.popleft()
	# 		if node.children == []:
	# 			queue.append(node)
	# 		else:
	# 			nodesToExplore.extend(node.children)
	# 	# build children, still BFS order
	# 	while(time.time() < t_zero + 4.):
	# 		node = queue.popleft()
	# 		children = node.build_children()
	# 		queue.extend(children)

	# def get_right_child(self, bitboard):
	# 	for child in self.children:
	# 		if bitboard.equals(child.bitboard):
	# 			return child
	# 	return None
