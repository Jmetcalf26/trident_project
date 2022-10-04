Required dependencies:
	apt: clang, python3-clang
	pip: clang, astor 
To install required dependencies: 
	run setup.sh script
To import python ast:
	from ast import *
To import c ast:
	import clang.cindex
To run main parser program with default input file of simple.c and relaxed type constraints:
	./parser.py
To run main parser program with strict typing:
	./parser.py -s
To run main parser program with custom input program:
	./parser.py -i <input-filename>
