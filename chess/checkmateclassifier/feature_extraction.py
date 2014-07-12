import sys
from collections import defaultdict
import re
import chess

def fen_to_piece_placement_array(fen):
	piece_placement = fen.split()[0]
	piece_placement_array = [list(line) for line in piece_placement.split("/")]
	piece_placement_array1 = []
	for line in piece_placement_array:
		new_line = []
		for char in line:
			try:
				number=int(char)
				new_line.extend([0]*number)
			except:
				new_line.append(char)

		piece_placement_array1.append(new_line)
	return piece_placement_array1

def get_count_features(piece_placement_array):
	counters = defaultdict(int)
	pieces= set()
	for i,row in enumerate(piece_placement_array):
		for j,piece in enumerate(row):
			counters["total"] += int(piece!=0)
			if piece== 0:
				continue
			piece_lower = piece.lower()
			#black is lower case
			is_white = piece_lower != piece
			counters["white"] += int(is_white)
			counters["black"] += int(not is_white)
			counters["single_side_"+piece]+=1
			counters[piece_lower]+=1
			if piece_lower in ["p"]:
				continue
			pieces.add(piece)
			#"king or a queen"
			for k in xrange(max(0,i-3), min(i+4,8)):
				for l in xrange(max(0,j-3), min(j+4,8)):
					if k == i and j == l:
						continue
					other_piece = piece_placement_array[k][l]
					if other_piece == 0:
						for d in range(1,4):
							if  i-d <= k <= i +d and  j-d <= l <= j+d:
								counters["single_side_"+piece+"_empty_"+str(d)]+=1
						continue
					is_other_white = other_piece != other_piece.lower() 
					
					for d in range(1,4):
						if  i-d <= k <= i +d and  j-d <= l <= j+d:
							counters["single_side_"+piece+"_same_side_"+str(d)]+= int(is_white == is_other_white)
							counters["single_side_"+piece+"_other_side_"+str(d)]+= int(is_white != is_other_white)

	for piece in pieces:
		if "single_side_"+piece not in counters:
			continue
		for d in range(1,4):
			other_side_d = counters["single_side_"+piece+"_other_side_"+str(d)]
			same_side_d = counters["single_side_"+piece+"_same_side_"+str(d)]
			empty_d = counters["single_side_"+piece+"_empty_"+str(d)]
			counters["single_side_"+piece+"_threat_"+str(d)] = 1+int(other_side_d >= same_side_d  )
			counters["single_side_"+piece+"_mostly_empty_"+str(d)] = 1+int(empty_d >  other_side_d + same_side_d)
			counters["single_side_"+piece+"_mostly_more_empty_than_good_"+str(d)] = 1+int(empty_d >  same_side_d)
			counters["single_side_"+piece+"_mostly_more_empty_than_bad_"+str(d)] = 1+int(empty_d >  other_side_d)
			counters["single_side_"+piece+"_other_side_exist_"+str(d)] = 1+int(other_side_d > 0)
	return counters

def get_feature_headers():
	general= ["total","white","black"]
	pieces= ["b","k","n","p","q","r"]
	single_side_features = []
	for piece in pieces:
		for p  in [piece, piece.upper()]:
			single_side_features.append("single_side_" + p)
			for d in range(1,4):
				single_side_features.append("single_side_"+p+"_empty_"+str(d))
				single_side_features.append("single_side_"+p+"_same_side_"+str(d))
				single_side_features.append("single_side_"+p+"_other_side_"+str(d))
				single_side_features.append("single_side_"+p+"_threat_"+str(d))
				single_side_features.append("single_side_"+p+"_mostly_empty_"+str(d))
				single_side_features.append("single_side_"+p+"_mostly_more_empty_than_good_"+str(d))
				single_side_features.append("single_side_"+p+"_mostly_more_empty_than_bad_"+str(d))
				single_side_features.append("single_side_"+p+"_other_side_exist_"+str(d))
	return general + pieces + single_side_features

def main(argv):
	'''
	Process pgn file - ignores meta data.
	For each move in the game prints a line - 
	piece which moved\tboard status before move\tboard status after move
	'''
	game_start = False
	
	features_headers= get_feature_headers()
	print "fen\t"+"\t".join(features_headers) + "\tis_game_over\tis_checkmate\tis_stalemate" 
	for line in sys.stdin:
		fen, results = line.strip().split("\t",1)
		piece_placement_array = fen_to_piece_placement_array(fen)
		count_features = get_count_features(piece_placement_array)
		new_line = fen +"\t"
		for feature in features_headers:
			new_line+= str(count_features[feature])+"\t"
		new_line+=results
		print new_line


if __name__ == '__main__':
	sys.stderr.write("Chess data extractor arguments: %s\n"%sys.argv)
	main(sys.argv)