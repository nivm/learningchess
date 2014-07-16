import re,sys

def main(argv):	
	for line in sys.stdin:
		piece,from_location,to_location, surround = line.split("\t")
		fields = line.strip().split("\t")
		if len(fields)==4:
			piece, from_location, to_location, surround = fields
		elif len(fields)==3:
			piece, from_location, to_location = fields
		else:
			continue
		from_location = from_location.split(",")
		to_location = to_location.split(",")
		if len(fields)==4:
			print "%s\t%s\t%s\t%s" % (piece, int(to_location[0])-int(from_location[0]), 
				int(to_location[1]) - int(from_location[1]), surround)
		else:
			print "%s\t%s\t%s\t" % (piece, int(to_location[0])-int(from_location[0]), 
				int(to_location[1]) - int(from_location[1]))
		
if __name__ == '__main__':
	sys.stderr.write("Calculate move diff: %s\n"%sys.argv)
	main(sys.argv)