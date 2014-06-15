import sys
import re
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt

pieces_hash = {"r": "rook", "k": "king", "q": "queen", "b" : "bishop", \
"n" : "knight", "p" : "pawn"}

def normalize_area_vec (piece_area):
	normalization_factor = 1000.0 / sum(piece_area)
	piece_area = [normalization_factor * p for p in piece_area]
	return piece_area

def draw_charts(chess_pieces_move_dict):

	for piece, piece_moves in chess_pieces_move_dict.iteritems():
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.set_title(pieces_hash[piece])
		piece_x = []
		piece_y = []
		piece_area = []
		for locations, count in piece_moves.iteritems():
			piece_x.append(locations[0])
			piece_y.append(locations[1])
			piece_area.append(count)
		piece_area = normalize_area_vec(piece_area)
		plt.scatter(piece_x, piece_y, s=piece_area, alpha=0.5)
		ax.set_xticks(range(min(piece_x)-1,max(piece_x)+2))
		ax.set_yticks(range(min(piece_y)-1,max(piece_y)+2))
		plt.grid(b=True, which='both', color='0.65',linestyle='-')
		plt.show()

def main():
	'''
	Draw a histogram of the relative movments of the pieces
	Input count piece x y
	'''
	chess_pieces_move_dict = defaultdict(lambda : defaultdict(int))
	for line in sys.stdin:
		count, piece, x,y = re.split("\s", line.strip())
		x = int(x)
		y = int(y)
		count = int(count)

		# piece is in lower case to ignore black \ white differences
		chess_pieces_move_dict[piece.lower()][(x,y)]+= count
	draw_charts(chess_pieces_move_dict)


if __name__ == '__main__':
	main()