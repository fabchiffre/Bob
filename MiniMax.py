from board import *

def minimax(board, depth):
	best_move = None
	bord.generate
	for m in board.moves:
		m.apply
		m.score = mini(board, depth-1)
			if(best_move == None or best_move.score > m.score):
			best_move = m
		m.undo
	return best_move

def maxi(board, depth, my_team):
	if (depth == 0):
		return board.compute_heuristic_value(my_team)

	max_move = None
	board.generate
	for m in board.moves:
		m.apply
		m.score = mini(board, depth -1)
		if(max_move == None or max_move.score < m.score):
			max_move = m
		m.undo
	return max_move.score

def mini(board, depth, my_team):
	if (depth == 0):
		m.score = board.compute_heuristic_value(my_team)

	min_move = None
	board.generate
	for m in board.moves:
		m.apply
		m.score = max(board, depth -1)
		if(min_move == None or min_move.score > m.score):
			min_move = m
		m.undo
	return min_move.score