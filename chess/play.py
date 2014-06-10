import re,sys
import chess

def is_game_over(play_str):
	try:
		plays = sum([x.split() for x in re.split("[0-9]*\.", play_str) if x], [])[:-1]
		board = chess.Bitboard()
		for play in plays:
			board.push_san(play)
		return board.is_game_over()
	except:
		#print play_str
		#print plays
		#print "PLAY:  "+play
		raise



pgn_file=open("../data/IB1419.pgn")

play=""
counter = 0
for line in pgn_file:
	line = line.strip("\n")
	line = line.strip("\r")
	if line.startswith("["):
		continue

	if not line and play:
		game_over = is_game_over(play)
		counter += 1
		if game_over:
			print str(counter) + "\t" + play + "\t" + str(game_over)
			print "#"*20 
		play="" 
	else:
		play+=" " +line

	if (counter == 1000):
		break