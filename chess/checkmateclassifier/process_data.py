import sys
import chess
import re

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



def main(argv):
	'''
	Process pgn file - ignores meta data.
	For each move in the game prints a line - 
	piece which moved\tboard status before move\tboard status after move
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
			try:
				print_game(game)
			except:
				sys.stderr.write(str(game)+"\n")
			game_start = False
	
				

if __name__ == '__main__':
	sys.stderr.write("Chess data extractor arguments: %s\n"%sys.argv)
	main(sys.argv)