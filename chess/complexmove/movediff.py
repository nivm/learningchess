import re,sys

def main(argv):	
	for line in sys.stdin:
		piece,from_location,to_location, surround = line.split("\t")
		from_location = from_location.split(",")
		to_location = to_location.split(",")
		print "%s\t%s\t%s\t%s" % (piece, int(to_location[1])-int(from_location[1]), 
			int(to_location[0]) - int(from_location[0]), surround.strip() )
		
if __name__ == '__main__':
	sys.stderr.write("Calculate move diff: %s\n"%sys.argv)
	main(sys.argv)