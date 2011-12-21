# So I have no idea where to start from.
# Let us test the waters first. Start with hello World.
import sys		# Have to get the system file import. This would do the argument length thing.


# Write down list check the file for correctness. No other characters than *, ., S, and G.
# All lines are equal. That should do the trick for now.
def readMazeFile( mazeF ):
	filestate = open( mazeF, 'r' )	# The read mode for reading of the file.
	length = len( filestate.readline() ) - 1 	# Length of first line is to be standard and compared. -1 factor for rstrip newline.
	filestate.seek( 0, 0 )	# In last line I missed one line so will have to go over to beginning.
	state = ['pass']			# State is the list of lists that should have the success or failure message and the rest of the board state.
	for lines in filestate:
		temp = []	# Make a temporary list that will hold all the state variables for the processing.
		lines = lines.rstrip( '\n' )
		if len( lines ) != length :		# So if the line in question is not same length as first then there is error in file.
			print( 'The number of spaces in board is not consistent.' )
			state[0] = 'fail'	# You want the zeroth element of state to be read as success or failure.
			return state
		else :
			for ch in lines :
				if not (ch == 'S' or ch == 'G' or ch == '*' or ch == '.') :	# Only these characters are allowed in the file.
					print( 'Board contains invalid characters.' )
					state[0] = 'fail'
					return state
				else :
					temp.append( ch )
		state.append( temp )
	filestate.close()	# Do not forget to close the file.
	return state

# Now put up the main program code. So this dude is working. Now what. 
# Ofcourse do the file function of the state. But what exactly do I want to do.
def main():
	if len(sys.argv) != 2:
		print('Usage: python3.2 rolldice.py puzzle#.txt')
		return
	else:
		maze = readMazeFile( sys.argv[1] )
		print( maze )

# Execute the main program. So I would not guess just copy the code from previous programming assignment.
# So this becomes the starting point.
main()
