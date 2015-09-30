from board import *

alpha = 0.
beta = 0.

def alphabeta(board, depth):
	best_move = None
	global alpha = float('inf')
	global beta  = float('-inf')
	for m in board.generate():
		print "Search a move"
		m.apply
		m.score = mini(board, depth-1)
		if(best_move == None or best_move.score > m.score):
			best_move = m
		m.undo
	return best_move

def mini(board, depth):
	global alpha
	global beta
	if (depth == 0):
		return board.compute_heuristic_value(board.my_team)
	val = float('inf')
	moves = board.generate()
	for m in moves:
		m.apply
		score = maxi(board, depth-1)
		m.undo
		val = min(score, val)
		if (val <= alpha):
			return val
		beta = max(beta, val)
	return val

def maxi(board, depth):
	global alpha
	global beta
	if (depth == 0):
		return board.compute_heuristic_value(board.my_team)
	val = float('-inf')
	moves = board.generate()
	for m in moves:
		m.apply
		score = maxi(board, depth-1)
		m.undo
		val = max(score, val)
		if (val >= beta):
			return val
		alpha = max(alpha, val)
	return val


