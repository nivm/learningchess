Simple Move
===========

This approch try to calculate every chess piece move independed of other pieces and the board state.

Assumptions:

*. board 
*. ....


Execute:

./run.sh

will output the results file to stdout

Files:

*. simplemove.py - parse chess lines and output simple grid move for each piece.

simplemove.py is a pipe command line tool.
input: 
3 fields tab seprated lines  
piece from_fen to_fen

Example:
"P	rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1	rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1"

FEN  - http://en.wikipedia.org/wiki/Forsyth-Edwards_Notation

output:
3 fields tab seprated lines
piece from_grid_cordients  to_grid_cordients

Example:


*. movediff.py -  Calculate the difference in x,y axis of the move. I.e. pawn moving from c3->c4 would result - pawn 0 1


Results
-------

can be found at ../../data/results/simplemove/
