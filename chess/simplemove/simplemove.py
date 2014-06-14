import re,sys
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
				new_line.extend([1]*number)
			except:
				new_line.append(char)

		piece_placement_array1.append(new_line)
	return piece_placement_array1

def find_from_to(piece, from_piece_placement_array, to_piece_placement_array):
	from_location=()
	to_location=()
	for i in xrange(8):
		for j in xrange(8):
			if to_piece_placement_array[i][j] != from_piece_placement_array[i][j]:
				if piece == from_piece_placement_array[i][j]:
					from_location= (i,j)
				if piece == to_piece_placement_array[i][j]:
					to_location = (i,j)
	return from_location,to_location

def main(argv):
	'''
	parse chess output to a simple move file
	'''
	#line="P	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1	rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1"
	#line ="Q	k1r5/p1q4P/3p4/3P4/5PP1/2pQ2K1/2R5/8 w - - 3 45	k1r4Q/p1q5/3p4/3P4/5PP1/2pQ2K1/2R5/8 b - - 0 45"
	#line should be formated as
	#piece from_fen to_fen
	#fen http://en.wikipedia.org/wiki/Forsyth-Edwards_Notation
	
	for line in sys.stdin:
		try:
			piece,from_fen,to_fen = line.split("\t")
			to_piece_placement_array = fen_to_piece_placement_array(from_fen)
			from_piece_placement_array = fen_to_piece_placement_array(to_fen)
			from_location, to_location = find_from_to(piece, from_piece_placement_array, to_piece_placement_array)
			print "%s\t%s,%s\t%s,%s" % (piece, from_location[0],from_location[1] , to_location[0], to_location[1])
		except:
			pass
			#sys.stderr.write("Error: " + line + "\n")		

if __name__ == '__main__':
	sys.stderr.write("parse simple moves: %s\n"%sys.argv)
	main(sys.argv)
