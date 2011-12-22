import sys		# To do the picking up of the arguments. 
import math		# To do the math in heuristic functions.

# Input file sanity check. No other characters than *, ., S, and G. All lines are equal.
# Other conditions are one S and G only and any number of . and *. Those are unimplemented.
def readMazeFile( mazeF ):
	filestate = open( mazeF, 'r' )	# The read mode for reading of the file.
	length = len( filestate.readline() ) - 1 	# Length of first line is to be standard and compared. -1 factor for rstrip newline.
	filestate.seek( 0, 0 )		# In last line I missed one line so will have to go over to beginning.
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

# Return the orientation of initial die.
def startDie():
	return ['u','n','e','w','s','d']	# 1=up, 2=north, 3=east, 4=west, 5=south, 6=down

# Check the die on goal state is 1.
def isGoalDie( die ):
	if die.index('u') == 0 :	# I do not care about other faces. Face 1 should be only be up.
		return True
	else:
		return False

# Check for the valid move that is face 6 should not be up.
def isValidDie( die ):
	if die[5] == 'u' :
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

# Right now implementing the a_star algorithm verbatim from the course textbook code base. 
def a_star(maze, f):
    # f = memoize(f, 'f')
	# There are two things for the initial state. 1. Start state position 2. Correct orientation of dice.
    # node = Node(problem.initial)
	s_row, s_col = findStatePos( maze, 'S' )	# Get the start cordinates from the maze.
	die = startDie()
	# Ok the difficult part starts now. I can do the goal test, but what do I return.
	# There are more difficult parts to deal with. The way this algorithm works is more like BFS you go from state to state,
	# not node to node. The child state of the node will be the one that you get on a roll to a correct cell with correct state of die.
	# What I need from the problem will be the list of transitions it made.
    if problem.goal_test(node.state):
        return node
    frontier = PriorityQueue(min, f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
    return None

# Till now the function takes the input problem file.
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
	g_row, g_col = findStatePos( maze, 'G' )
	h1 = eDistance( g_row, g_col )		# Heuristic 1 a function that gives straight line distance from goal from present cordinates.
	h2 = mDistance( g_row, g_col )		# Heuristic 2 a function that gives manhattan distance from goal.
	s_row, s_col = findStatePos( maze, 'S' )
	# print( "heuristic 1 euclidean distance " + str( h1( s_row, s_col) ) )
	# print( "heuristic 1 manhattan distance " + str( h2( s_row, s_col) ) )
	# A* is best first search with the heuristic. How do I send the present cost of 0 to the function.
	a_star( maze, lambda cost, x, y : cost + h1(x, y) )

# The starting point for the program.
main()
