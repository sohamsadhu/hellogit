#!/bin/bash
puzzle=( puzzle1.txt puzzle2.txt puzzle3.txt puzzle4.txt puzzle5.txt )	# Create the array of puzzle files to be tested.
echo `touch testresults.txt`											# Create the test file of results if not present.
echo `cat /dev/null > testresults.txt`									# Empty the said file of any trash content.
for(( i = 0 ; i < 5 ; i++ )) ;
	do
		echo `python3.2 rblock.py ${puzzle[${i}]} >> testresults.txt` 
	done
