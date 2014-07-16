import sys
import re
from collections import defaultdict
import itertools
from math import sqrt

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
	histogram = {k : dict(v) for k,v in histogram.iteritems() if k!=4}
	#histogram = {k : dict(v) for k,v in histogram.iteritems() if len(v)==1 and k!=4}	
	return histogram

def rotate_surround(surround):
	'''
	Rotate surrond so white surround and black
	surround would act the same
	'''
	surround = surround.split(";")
	n = int(sqrt(len(surround)))
	surround = [surround[i:i+n] for i in xrange(0, n*n,n)]
	surround = [reversed(z) for z in reversed(surround)]
	surround = list(itertools.chain(*surround))
	surround = ";".join(surround)
	return surround

def group_by_histograms(histograms):
	histogram_groups = defaultdict(lambda: defaultdict(list))
	for piece, diffs in histograms.iteritems():
		for (x,y), histogram in diffs.iteritems():
			
			count = set(itertools.chain(*[k.values() for k in histogram.values()])).pop()
			# Random threshold
			if count < 10:
				continue
			histogram_groups[piece][tuple(histogram.keys())].append(((x,y),count))
	return histogram_groups

def main():
	'''
	Draw a histogram of the relative movments of the pieces
	Input count piece x y
	'''
	chess_pieces_move_dict = {}
	#
	for line in sys.stdin:
		fields = re.split("\t", line.strip())
		if len(fields)==3:
			piece, x,y = fields
		elif len(fields)==4:
			piece, x,y, surround = fields
		x = int(x)
		y = int(y)

		# Adjust black and white behaviour
		if piece.lower() != piece:
			x = -x
			y = -y
			if surround:
				surround = rotate_surround(surround)
		
		if piece.lower() not in chess_pieces_move_dict:
			if surround:
				chess_pieces_move_dict[piece.lower()] = \
				defaultdict(lambda : defaultdict(int))
			else:
				chess_pieces_move_dict[piece.lower()]= defaultdict[(x,y)]
		if surround:
			chess_pieces_move_dict[piece.lower()][(x,y)][surround]+= 1
		else:
			chess_pieces_move_dict[piece.lower()][(x,y)]+= 1

	histograms = defaultdict(lambda: defaultdict(dict))
	for piece in chess_pieces_move_dict:
		for x,y in chess_pieces_move_dict[piece]:			
			histogram = surrounds_histograms(chess_pieces_move_dict[piece][(x,y)])
			if histogram:
				histograms[piece][(x,y)] = histogram

	histogram_groups = group_by_histograms(histograms)
	for piece, piece_groups in histogram_groups.iteritems():
		for group, moves in piece_groups.iteritems():
			print piece,'\t',group,'\t',moves
	
	print '\n\n\n'
	for piece, diffs in histograms.iteritems():
		for (x,y), histogram in diffs.iteritems():
			print piece,'\t',(x,y),'\t',histogram
	#draw_charts(chess_pieces_move_dict)
	#draw_overall_chart(chess_pieces_move_dict)


if __name__ == '__main__':
	main()