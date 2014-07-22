import re,sys
import chess

import argparse

def fen_to_piece_placement_array(fen):
	'''
	return a 8X8 which represntation the board
	'''
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

def find_from_to(piece, from_array, to_array):
	'''
	Retruns (x1, y1), (x2,y2) which represnts the movement of the piece
	from from_array to to_array
	'''
	from_location=()
	to_location=()
	for i in xrange(len(from_array)):
		for j in xrange(len(from_array)):
			if to_array[i][j] != from_array[i][j]:
				if piece == from_array[i][j]:
					from_location= (j,i)
				if piece == to_array[i][j]:
					to_location = (j,i)
	return from_location,to_location

def find_surround(location, board_array, radius=1):
	'''
	Construct list representing the surrounding of radius
	x - spot is occiupied
	y - spot is clear
	z - spot is out of the board
	o - piece itself

	example - [y,y,z,y, o, z, z, z, z]
	This is the surround of radius 1 for the right
	whie rook on the opening position
	'''
	x,y = location[0], location[1]
	surround = []
	for i in xrange(-radius, radius+1):
		for j in xrange(-radius, radius+1):
			try:
				if j==0 and i == 0:
					surround.append("o")
					continue
				if board_array[y+i][x+j]==1:
					surround.append("y")
				else:
					surround.append("x")
			except:
				surround.append("z")
	return surround

def parseArguments(args):

	argprs = argparse.ArgumentParser(description="Simple move", add_help=True)

	argprs.add_argument('--radius', required=False, type=int, dest='radius', 
						help='Surround radius', default=1)

	arguments = argprs.parse_args(args)
	return arguments

def print_board_diff (board1, board2):
	for i in xrange(0, len(board1)):
		print board1[i], '\t',board2[i]

def main(argv):
	'''
	parse chess output to a simple move file
	'''
	arguments = parseArguments(argv[1:])
	
	for line in sys.stdin:
		try:
			piece,from_fen,to_fen = line.split("\t")
			from_piece_placement_array = fen_to_piece_placement_array(from_fen)
			to_piece_placement_array = fen_to_piece_placement_array(to_fen)
			from_location, to_location = find_from_to(piece, \
				from_piece_placement_array, to_piece_placement_array)

			surround = find_surround(from_location, from_piece_placement_array,\
				arguments.radius)

			print "%s\t%s,%s\t%s,%s\t%s" \
			% (piece, from_location[0],from_location[1] , \
				to_location[0], to_location[1], ";".join(surround))
		except:
			pass

if __name__ == '__main__':
	sys.stderr.write("parse simple moves: %s\n"%sys.argv)
	main(sys.argv)
