Required dependencies:

	apt: clang, python3-clang
	pip: clang, astor 
	
To install required dependencies: 

	./setup.sh
	
To import python ast (as used in parser.py):

	from ast import *
	
To import c ast (as used in parser.py):

	import clang.cindex
	
To run main parser program with default input file of simple.c and relaxed type constraints:

	./parser.py
	
To run main parser program with strict typing:

	./parser.py -s
	
To run main parser program with custom input program:

	./parser.py -i <input-filename>
	
