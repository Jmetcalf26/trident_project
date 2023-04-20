mapfile -t suffixes < <(ls testcases/ | grep $1 | rev | cut -d'_' -f1 | rev)
mapfile -t files < <(ls testcases/ | grep $1)
if [ $# -ne 1 ]; then
	echo "Usage: ./eval_testcases.sh <test files prefix>"
	echo "  Example: ~/C/testcases/CWE_121_... ./gen_bulk_tests CWE242 combo_file"
else
	for (( i=0; i<${#files[@]}; i++ )); do
		echo "****************** ${files[$i]} ******************"
		./main.py -t -i testcases/${files[$i]} -o $1_PYTHON_${suffixes[$i]} > /dev/null
		python3 $1_PYTHON_${suffixes[$i]}.py 
		echo "exit code: $?"
		echo "*****************************************************************"
	done
fi
