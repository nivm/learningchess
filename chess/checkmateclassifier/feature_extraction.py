import sys
from collections import defaultdict
import re
import chess

def print_game(game):
	'''
	print Game data and moves
	'''
	game = " ".join(game)
	game = re.sub("\d+\.", " ", game).strip()
	moves = re.split("\s+", game)
	board = chess.Bitboard()
	
	end = moves[-1]
	moves = moves[:-1]
	
	after_str = str(board)
	for move in moves:
		mv = board.push_san(move)
		after_str = str(board)
		# Piece that moved
		#piece = board.piece_at(mv.to_square)
		
		sys.stdout.write("%s\t%s\t%s\t%s\n"%(after_str, board.is_game_over(), board.is_checkmate(), board.is_stalemate()))

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
	for row in piece_placement_array:
		for piece in row:
			counters["total"] += int(piece!=0)
			if piece!= 0:
				piece_lower = piece.lower()
				counters["white"] += piece_lower != piece
				counters["black"] += piece_lower == piece
				counters["single_side_"+piece]+=1
				counters[piece_lower]+=1
	return counters

def main(argv):
	'''
	Process pgn file - ignores meta data.
	For each move in the game prints a line - 
	piece which moved\tboard status before move\tboard status after move
	'''
	game_start = False
	
	features_headers= ["total","white","black","b","k","n","p","q","r","single_side_b","single_side_B","single_side_k","single_side_K","single_side_n","single_side_N","single_side_p","single_side_P","single_side_q","single_side_Q","single_side_r","single_side_R"]
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