import sys		  # To do the picking up of the arguments. 
import math		  # To do the math in heuristic functions.
import copy		  # Have to do this for the list copy.

# Input file sanity check. No other characters than *, ., S, and G. All lines are equal.
# Other conditions are one S and G only and any number of . and *. Those are unimplemented.
def readMazeFile( mazeF ):
	filestate = open( mazeF, 'r' )	# The read mode for reading of the file.
	width = len( filestate.readline() ) - 1 	# Length of first line is to be standard and compared. -1 factor for rstrip newline.
	filestate.seek( 0, 0 )		# In last line I missed one line so will have to go over to beginning.
	state = ['pass']			# State is the list of lists that should have the success or failure message and the rest of the board state.
	for lines in filestate:
		temp = []	# Make a temporary list that will hold all the state variables for the processing.
		lines = lines.rstrip( '\n' )
		if len( lines ) != width :		# So if the line in question is not same length as first then there is error in file.
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

# Return the initial die with start cordinates, initial position, path cost and empty list of actions. These all are individual lists.
# This is supposed to be my problem representation or the node that I will evaluate.
def startDie( x, y ):
	return [ [ x, y ], ['u','n','e','w','s','d'], [ 0 ], [] ]	# 1=up, 2=north, 3=east, 4=west, 5=south, 6=down

# Check the die on goal state is 1.
def isGoalDie( die ):
	if die[1].index('u') == 0 :	# I do not care about other faces. Face 1 should be only be up.
		return True
	else:
		return False

# Check for the valid move that is face 6 should not be up.
def isValidDie( die ):
	if die[5] == 'u' :
		return False
	else:
		return True

# Check if the given cell is valid.
def isValidCell( row, col, maze ):
	if maze[row][col] == '*' :
		return False
	else:
		return True

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

# Heuristic for the straight line or the euclidean distance.
def eDistance( x1, y1 ):
	return lambda x2, y2 : math.sqrt( (x1 - x2)**2 + (y1 - y2)**2 )

# Get the heuristic of the Manhattan distance.
def mDistance( x1, y1 ):
	return lambda x2, y2 : math.fabs(x1 - x2) + math.fabs(y1 - y2)

# Find the cordinates of the start and goal states in the list of lists.
def findStatePos( maze, state ):
	x, y = 0, 0							# The x and y cordinate abstraction of list where the state thing could be.
	for row in maze:					# Try to find in each list or the row of the maze the said goal state
		try:							# Since index on list can give ValueError if not present have to handle
			y = row.index( state )  	# that error.
			return x, y
		except ValueError:
			pass						# Don't do anything on error, just continue
		x = x + 1
	return x, y

# Function that will see if goal has been achieved or not.
def goalTest( maze, die ):
	g_row, g_col = findStatePos( maze, 'G' )
	if g_row == die[0][0] and g_col == die[0][1] and isGoalDie( die ) :
		return True
	else:
		return False

# Function that will tell if the two lists are equivalent or not. Ok I am interested in only first two lists of the lists sent.
def isPresent( die, explored ):
	if len( explored ) > 0 :
		for element in explored:
			if die[0] == element[0] and die[1] == element[1] :
				return True
		return False	# Could not find the element in the list.
	else:
		return False	# If set is empty then the element is not present.

# This function solely works on the assumption that the child exists in anylist. If it does not I do not send any error message.
def findIndex( anylist, child ):
	index = 0
	for element in anylist:
		if child[0] == element[0] and child[1] == element[1] :
			return index
		else:
			index = index + 1

# The priority queue poping up function.
def popElement( frontier, f ):
	index, counter, min = 0, 0, 1000000
	for element in frontier:
		if f( element ) < min :		# This makes sure that first element with min value gets selected.
			min = f( element )		# A element with value equal to this element but later in the list will not be selected.
			index = counter
		else:
			counter = counter + 1
	return frontier.pop( index )	# Since lists work as referenced objects so this statement actually removes child from frontier.

# Ok now have to do the expand thing in the nodes for the list. That is given the die and the problem. I will have to figure out the valid moves it 
# can take and then make it do them and then return the list of both the dice in the list that will be thrown back.
def getChildren( die, maze ):
	rolls = []	# A list that will be returned with all the children dice moves.
	# Now what you need you need the positions and then decide where you can move.
	#	N       'You can move in this direction if row > 0
	# W   E	    'You can move W if col > 0 and towards col < width - 1
	#	S		'You can move towards S if row < length - 1
	if die[0][0] > 0 : # Move North. Check the north cell.
		if isValidCell( die[0][0] - 1 , die[0][1], maze ) :	# If the north cell is valid then roll die north.
			ndie = copy.deepcopy( die )	# Have to get this extra variable else all the guys change the same thing.
			if isValidDie(rollDice( ndie[1], 'N') ) :	# Check if the north roll gives a valid die. Since lists are reference this already changes orientation.
				ndie[0][0] = ndie[0][0] - 1		# Update the cordinates
				# ndie[1] = rollDice( die[1], 'N' )	# Give the new updated dice state.
				ndie[2][0] = ndie[2][0] + 1		# Increment the cost that you have occured till now.
				ndie[3].append('N')				# Append the action you took into the list.
				rolls.append( ndie )			# Lastly append the die on the return children list.
	if die[0][1] > 0 : # Move West
		if isValidCell( die[0][0], die[0][1] - 1 , maze ) :	# Now peek into the west cell.
			wdie = copy.deepcopy( die )
			if isValidDie(rollDice( wdie[1], 'W') ) :	# Check if the west roll gives a valid die. This also changes the orientation of die since it's referenced.
				wdie[0][1] = wdie[0][1] - 1
				wdie[2][0] = wdie[2][0] + 1
				wdie[3].append('W')
				rolls.append( wdie )	
	if die[0][1] < len( maze[0] ) - 1 : # Move East
		if isValidCell(die[0][0], die[0][1] + 1 , maze ) :	# Now peek into the east cell.
			edie = copy.deepcopy( die )
			if isValidDie( rollDice( edie[1], 'E') ) :	# Check if the east roll gives a valid die.
				edie[0][1] = edie[0][1] + 1
				edie[2][0] = edie[2][0] + 1
				edie[3].append('E')
				rolls.append( edie )
	if die[0][0] < len( maze ) - 1 :	# Move South
		if isValidCell(die[0][0] + 1 , die[0][1], maze ) :	# Now peek into the south cell.
			sdie = copy.deepcopy( die )
			if isValidDie( rollDice( sdie[1], 'S') ) :	# Check if the south roll gives a valid die.
				sdie[0][0] = sdie[0][0] + 1
				sdie[2][0] = sdie[2][0] + 1
				sdie[3].append('S')
				rolls.append( sdie )
	return rolls	# Lastly return the children.

# Right now implementing the a_star algorithm verbatim from the course textbook code base. 
def a_star(maze, f):
	# There are two things for the initial state. 1. Start state position 2. Correct orientation of dice.
	s_row, s_col = findStatePos( maze, 'S' )	# Get the start cordinates from the maze.
	die = startDie( s_row, s_col )
	if goalTest( maze, die ):
		return die
	frontier = [ die ]		# You want the priority queue to be a list that you will try to insert and sort the elements.
	explored = []			# Do not have to make a set a empty list will do the trick just have to check and append.
	while frontier:
		# die = frontier.pop( 0 )		# Get the first element from the list, that will be sorted as priority queue.
		die = popElement( frontier, f )	# The heuristic is required so that it can pop out the element with least value, since list unsorted.
		if goalTest( maze, die ):
			return die
		explored.append( die )
		for child in getChildren( die, maze ):
			if not(isPresent( child, explored )) and not(isPresent( child, frontier )):
				frontier.append( child )
			elif isPresent( child, frontier ):
				incumbent = frontier[ findIndex( frontier, child ) ]
				if f( child ) < f( incumbent ):
					frontier.pop( findIndex(frontier, incumbent) )	#del frontier[incumbent]
					frontier.append( child )
	return None

# This function takes the file checks for correctness. Gets the heuristics, and calls the astar function and prints results. 
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
	g_row, g_col = findStatePos( maze, 'G' )
	h1 = eDistance( g_row, g_col )		# Heuristic 1 a function that gives straight line distance from goal from present cordinates.
	h2 = mDistance( g_row, g_col )		# Heuristic 2 a function that gives manhattan distance from goal.
	s_row, s_col = findStatePos( maze, 'S' )
	# print( "heuristic 1 euclidean distance " + str( h1( s_row, s_col) ) )
	print()
	print( 'Results for puzzle file ' + sys.argv[1] )
	result = a_star( maze, lambda die: die[2][0] + h1(die[0][0], die[0][1]) )	# Calling the astar function with problem maze and  heuristic parameters.
	if type( result ) is type( None ):
		print( 'No solution was found to the problem, with straight line heuristics.' )
	else:
		print( 'Result with straight line heuristic ' )
		print( 'End orientation of the die is ' + str( result[1] ) )
		print( 'Path taken or the rolls of the die were in following order ' + str( result[3] ) )
		print( 'Cost of the path was '+ str( result[2][0] ) )
	result = a_star( maze, lambda die: die[2][0] + h2(die[0][0], die[0][1]) )	 # cost, x, y : cost + h1(x, y)
	print()
	if type( result ) is type( None ):
		print( 'No solution was found to the problem, with Manhattan distance heuristic.' )
	else:
		print( 'Result with Manhattan distance heuristic ' )
		print( 'End orientation of the die is ' + str( result[1] ) )
		print( 'Path taken or the rolls of the die were in following order ' + str( result[3] ) )
		print( 'Cost of the path was '+ str( result[2][0] ) )
	print( 'End Results for puzzle file ' + sys.argv[1] )
	print( )
	print( '==============================================================================================' )

# The starting point for the program.
main()
