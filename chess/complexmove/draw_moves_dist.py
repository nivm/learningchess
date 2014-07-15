import sys
import re
from collections import defaultdict
import itertools

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
		ax.set_title(pieces_hash[piece].upper() + " move histogram")
		piece_x = []
		piece_y = []
		piece_area = []
		for locations, count in piece_moves.iteritems():
			piece_x.append(locations[1])
			piece_y.append(locations[0])
			piece_area.append(count)
		piece_area = normalize_area_vec(piece_area)
		
		plt.scatter(piece_x, piece_y, s=piece_area, alpha=0.5)
		# Adding the piece it self
		plt.scatter([0], [0], s=200, alpha=0.6, color="red")
		ax.set_xticks(range(min(piece_x)-1,max(piece_x)+2))
		ax.set_yticks(range(min(piece_y)-1,max(piece_y)+2))
		plt.grid(b=True, which='both', color='0.65',linestyle='-')
		plt.show()


def draw_overall_chart (chess_pieces_move_dict):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	piece_color_hash = {"p": "LightSlateGray", "k": "Navy", "q":"ForestGreen",\
	"r": "OrangeRed", "n": "LimeGreen","b": "red"}
	
	legend,legend_text = [], []
	for i, (piece, piece_moves) in enumerate(chess_pieces_move_dict.iteritems()):
		#ax.set_title(pieces_hash[piece].upper() + " move histogram")
		piece_x = []
		piece_y = []
		piece_area = []
		#legend_text.append(pieces_hash[piece].upper())
		legend_text.append(pieces_hash[piece])
		for locations, count in piece_moves.iteritems():
			piece_x.append(locations[0])
			piece_y.append(locations[1])
			piece_area.append(count)
		piece_area = normalize_area_vec(piece_area)
		plt.scatter(piece_x, piece_y, alpha=0.75, \
			color=piece_color_hash[piece], s=piece_area)
		#print type(x), x.get_sizes()

		ax.set_xticks(range(min(piece_x)-1,max(piece_x)+2))
		ax.set_yticks(range(min(piece_y)-1,max(piece_y)+2))
		#, fontsize=8
	plt.legend(legend_text, scatterpoints=1,loc='lower center',ncol=6, prop={'size':10})
	plt.scatter([0], [0], s=180, alpha=0.9, color="black")
	plt.grid(b=True, which='both', color='0.65',linestyle='-')
	plt.show()

def surrounds_histograms(surrounds_data):
	histogram = defaultdict(lambda: defaultdict(int))
	for surround, count in surrounds_data.iteritems():
		elements = surround.split(";")
		for i in xrange(0, len(elements)):
			histogram[i][elements[i]]+=count
	histogram = {k : dict(v) for k,v in histogram.iteritems() if len(v)==1 and k!=4}
	return histogram

def main():
	'''
	Draw a histogram of the relative movments of the pieces
	Input count piece x y
	'''
	chess_pieces_move_dict = {}
	#
	for line in sys.stdin:
		count, piece, x,y, surround = re.split("\s", line.strip())
		x = int(x)
		y = int(y)
		count = int(count)

		# piece is in lower case to ignore black \ white differences
		if piece.lower() != piece:
			x = -x
			y = -y
			surround = surround.split(";")
			surround = [surround[:3],surround[3:6],surround[6:]]
			surround = [reversed(z) for z in reversed(surround)]
			surround = list(itertools.chain(*surround))
			surround = ";".join(surround)
		if piece.lower() not in chess_pieces_move_dict:
			chess_pieces_move_dict[piece.lower()] = defaultdict(lambda : defaultdict(int))
		chess_pieces_move_dict[piece.lower()][(x,y)][surround]+= count
	for piece in chess_pieces_move_dict:
		print piece
		for x,y in chess_pieces_move_dict[piece]:
			#if x <= 1 and x >= -1 and y <= 1 and y >= -1:
			#	continue
			histogram = surrounds_histograms(chess_pieces_move_dict[piece][(x,y)])
			if histogram:
				print "\t",x,y,'\t', histogram
			'''
			for surround in chess_pieces_move_dict[piece][(x,y)]:
				print "\t\t",surround,'\t',chess_pieces_move_dict[piece][(x,y)][surround]
			'''
	#draw_charts(chess_pieces_move_dict)
	#draw_overall_chart(chess_pieces_move_dict)


if __name__ == '__main__':
	main()