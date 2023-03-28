#!/bin/bash
if [ $# -ne 2 ]; then
	echo "Usge: ./testcase_generator.sh <testcase_file> <output_file>"
else
	cat my_io.c $1 > $2
	echo "created $2 file"
fi
