import sys
import re
from copy import deepcopy

import chess

CHESS_HASH = {"a1": chess.A1, "a2": chess.A2, "a3": chess.A3, "a4": chess.A4,\
 "a5": chess.A5, "a6": chess.A6, "a7": chess.A7, "a8": chess.A8,\
 "b1": chess.B1, "b2": chess.B2, "b3": chess.B3, "b4": chess.B4,\
 "b5": chess.B5, "b6": chess.B6, "b7": chess.B7, "b8": chess.B8,\
 "c1": chess.C1, "c2": chess.C2, "c3": chess.C3, "c4": chess.C4,\
 "c5": chess.C5, "c6": chess.C6, "c7": chess.C7, "c8": chess.C8,\
 "d1": chess.D1, "d2": chess.D2, "d3": chess.D3, "d4": chess.D4,\
 "d5": chess.D5, "d6": chess.D6, "d7": chess.D7, "d8": chess.D8,\
 "e1": chess.E1, "e2": chess.E2, "e3": chess.E3, "e4": chess.E4,\
 "e5": chess.E5, "e6": chess.E6, "e7": chess.E7, "e8": chess.E8,\
 "f1": chess.F1, "f2": chess.F2, "f3": chess.F3, "f4": chess.F4,\
 "f5": chess.F5, "f6": chess.F6, "f7": chess.F7, "f8": chess.F8,\
 "g1": chess.G1, "g2": chess.G2, "g3": chess.G3, "g4": chess.G4,\
 "g5": chess.G5, "g6": chess.G6, "g7": chess.G7, "g8": chess.G8,\
 "h1": chess.H1, "h2": chess.H2, "h3": chess.H3, "h4": chess.H4,\
 "h5": chess.H5, "h6": chess.H6, "h7": chess.H7, "h8": chess.H8}

def process_game(game):
	'''
	print Game data and moves
	'''
	game = " ".join(game)
	game = re.sub("\d+\.", " ", game).strip()
	moves = re.split("\s+", game)
	board = chess.Bitboard()
	
	end = moves[-1]
	moves = moves[:-1]
	
	after_board = board
	for move in moves:
		before_board = deepcopy(after_board)
		mv = board.push_san(move)
		after_board = board
		counter = 0

		for pos in CHESS_HASH:
			if str(after_board.piece_at(CHESS_HASH[pos])) != \
				str(before_board.piece_at(CHESS_HASH[pos])):
				'''
				sys.stdout.write("%s\t%s\t%s\n"%(pos, \
					before_board.piece_at(CHESS_HASH[pos]),\
					after_board.piece_at(CHESS_HASH[pos])))
				'''
				counter +=1
		sys.stdout.write("%s\t%s\t%s\n"%(before_board,after_board,counter))

def main(args):
	'''
	Process pgn file - ignores meta data.
	For each move in the game prints how many pieces changed their position
	board status before move\tboard status after move\t#pieces_moved
	'''
	game_start = False
	
	for line in sys.stdin:
		line = line.strip()
		if line and not line.startswith("["):
			if not game_start:
				game_start = True
				game = []
			game.append(line)
		elif game_start:
			process_game(game)
			game_start = False
			break

if __name__ == '__main__':
	sys.stderr.write("Chess data changes on board arguments: : %s\n"%sys.argv)
	main(sys.argv)