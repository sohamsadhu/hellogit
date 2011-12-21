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

# For the moment I am just writing a dice roll function. This function gets the dice list as position and the position
# to roll as the other argument and then returns back the list when rolled to that direction.
def rollDice( dice, direction ):
	# Python does not have a switch statement! Will have to do this the if elif way.
	if direction == 'N' :			   					# You roll on the north edge. Edges east and west do not change.
		iorient1 = dice.index('u') ; iorient2 = dice.index('n') # Get the index of the sides you want to change. 
		iorient3 = dice.index('s') ; iorient4 = dice.index('d')	# e = east, w = west, n = north, s = south, u = upper, d = down 
		dice[iorient1] = 'n' ; dice[iorient2] = 'd'				# Now change those indexes or directions.
		dice[iorient3] = 'u' ; dice[iorient4] = 's'
		return dice										# Dice orientation transformed. Now return the same.
	elif direction == 'E' :								# When you roll on the eastern or right edge. North and South face do not change.
		iorient1 = dice.index('e') ; iorient2 = dice.index('w')
		iorient3 = dice.index('u') ; iorient4 = dice.index('d')
		dice[iorient1] = 'd' ; dice[iorient2] = 'u'			
		dice[iorient3] = 'e' ; dice[iorient4] = 'w'
		return dice										
	elif direction == 'W' :								# Roll on western or left edge. Faces north and south do not change.
		iorient1 = dice.index('u') ; iorient2 = dice.index('e') 
		iorient3 = dice.index('w') ; iorient4 = dice.index('d') 
		dice[iorient1] = 'w' ; dice[iorient2] = 'u'	
		dice[iorient3] = 'd' ; dice[iorient4] = 'e'			
		return dice
	else : # direction == 'S'							  Roll downwards. East and West face do not change.
		iorient1 = dice.index('u') ; iorient2 = dice.index('n') 
		iorient3 = dice.index('s') ; iorient4 = dice.index('d') 
		dice[iorient1] = 's' ; dice[iorient2] = 'u'
		dice[iorient3] = 'd' ; dice[iorient4] = 'n'		
		return dice

# Now put up the main program code. So this dude is working. Now what. 
# Ofcourse do the file function of the state. But what exactly do I want to do.
def main():
	maze = []
	if len(sys.argv) != 2:
		print('Usage: python3.2 rolldice.py puzzle#.txt')
		return
	else:
		maze = readMazeFile( sys.argv[1] )
		if maze[0] == 'fail':
			print('There seems to be some error with input, please try again.')
			return		# The program has raised a failure and now halt the execution of the program.
	maze.pop(0)	# Remove the pass element so we can further process the same. So I get my maze as a list.
	dice = [ 'u', 'n', 'e', 'w', 's', 'd' ] # Each index of the list represents the number of the dice and letters stand 
			# for u = up, d = down, n = north, e = east, w = west, s = south. Right now the dice state represents the start position of dice.
	# Now check the dice roll function for correctness.
	# dice = rollDice( dice, 'N' )
	# print( 'After rolling it north' + str(dice) )


# Execute the main program. So I would not guess just copy the code from previous programming assignment.
# So this becomes the starting point.
main()
