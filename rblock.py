import sys		  # To do the picking up of the arguments. 
import math		  # To do the math in heuristic functions.
import heapq	  # Have to get the priority queue thing working.
import itertools  # Another one for the priority queue.

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
	if die[1][5] == 'u' :
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
	bcord, borient = False, False # cordinates and orientation boolean values.
	if len( explored ) > 0 :
		for element in explored:
			if die[0] == element[0] :
				bcord = True
			if die[1] == element[1] :
				borient = True
		return bcord and borient
	else:
		return False	# If set is empty then the element is not present.

# Global variables for the priority queue thingy.
entry_finder = {}				# Mapping of tasks to entries.
REMOVED = '<removed-task>'		# place holder for a removed task
counter = itertools.count() 	# unique sequence count

def pqadd(pq, task, priority):
	# Add a new task or update the priority of an existing task
    if task in entry_finder:
        pqremove(task)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    heappush(pq, entry)
	return pq

def pqremove(pq, task):
    # Mark an existing task as REMOVED.  Raise KeyError if not found.
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED

def pqpop(pq):
    # Remove and return the lowest priority task. Raise KeyError if empty.
    while pq:
        priority, count, task = heappop(pq)
        if task is not REMOVED:
            del entry_finder[task]
            return task
    raise KeyError('pop from an empty priority queue')

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
			if isValidDie( rollDice( die, 'N') ) :	# Check if the north roll gives a valid die.
				die[0][0] = die[0][0] - 1		# Update the cordinates
				die[1] = rollDice( die, 'N' )	# Give the new updated dice state
				die[2] = die[2] + 1				# Increment the cost that you have occured till now.
				die[3].append('N')				# Append the action you took into the list.
				rolls.append( die )				# Lastly append the die on the return children list.
	elif die[0][1] > 0 : # Move West
		if isValidCell( die[0][0], die[0][1] - 1 , maze ) :	# Now peek into the west cell.
			if isValidDie( rollDice( die, 'W') ) :	# Check if the west roll gives a valid die.
				die[0][0] = die[0][1] - 1
				die[1] = rollDice( die, 'W' )
				die[2] = die[2] + 1	
				die[3].append('W')
				rolls.append( die )	
	elif die[0][1] < len( maze[0] ) - 1 : # Move East
		if isValidCell( die[0][0], die[0][1] + 1 , maze ) :	# Now peek into the east cell.
			if isValidDie( rollDice( die, 'E') ) :	# Check if the east roll gives a valid die.
				die[0][0] = die[0][1] + 1
				die[1] = rollDice( die, 'E' )
				die[2] = die[2] + 1	
				die[3].append('E')
				rolls.append( die )
	elif die[0][0] < len( maze ) - 1 :	# Move South
		if isValidCell( die[0][0] + 1 , die[0][1], maze ) :	# Now peek into the south cell.
			if isValidDie( rollDice( die, 'S') ) :	# Check if the south roll gives a valid die.
				die[0][0] = die[0][0] + 1
				die[1] = rollDice( die, 'S' )
				die[2] = die[2] + 1
				die[3].append('S')
				rolls.append( die )
	return rolls	# Lastly return the children.

# Right now implementing the a_star algorithm verbatim from the course textbook code base. 
def a_star(maze, f):
    # f = memoize(f, 'f')
	# There are two things for the initial state. 1. Start state position 2. Correct orientation of dice.
    # node = Node(problem.initial)
	s_row, s_col = findStatePos( maze, 'S' )	# Get the start cordinates from the maze.
	die = startDie( s_row, s_col )
    # Ok write the goal test for this guy. What it will be. You send out the problem and your state in the die.
	if goalTest(die):
        return die
    # Damn even priority queue has not been made and I have to make it.
	frontier = pqadd( [], die, f( die[0][0], die[0][1] ) ) 
	explored = []	# Do not have to make a set a empty list will do the trick just have to check and append.
    while frontier:
        die = pqpop( frontier )
        if goalTest( die ):
            return die
		for child in getChildren( die, maze ):
            if not(isPresent( child, explored )) and not(isPresent( child, frontier )):
                pqadd( frontier, child, f(die[0][0], die[0][1]) )
            elif isPresent( child, frontier ):
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
