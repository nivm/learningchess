import chess
board = chess.Bitboard()
board.push_san("e4")
board.push_san("e5")
board.push_san("Qh5")
board.push_san("Nc6")
board.push_san("Bc4")
board.push_san("Nf6")
board.push_san("Qxf7")
print "is_checkmate: " +str(board.is_checkmate())
print "is_stalemate: " +str(board.is_stalemate())
print "is_insufficient_material: " +str(board.is_insufficient_material())
print "board.is_game_over: " + str(board.is_game_over())