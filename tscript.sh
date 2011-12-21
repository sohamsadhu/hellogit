#!/bin/bash
puzzle=( puzzle1.txt puzzle2.txt puzzle3.txt puzzle4.txt puzzle5.txt )
for(( i = 0 ; i < 5 ; i++ )) ;
	do
		echo `python3.2 rblock.py ${puzzle[${i}]}` 
	done
