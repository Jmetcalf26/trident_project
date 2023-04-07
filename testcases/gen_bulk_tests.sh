mapfile -t suffixes < <(ls $1 | grep $2 | rev | cut -d'_' -f1 | rev)
mapfile -t files < <(ls $1 | grep $2)
if [ $# -ne 3 ]; then
	echo "Usage: ./gen_bulk_tests <test files location> <input_prefix> <output_prefix>"
	echo "  Example: ~/C/testcases/CWE_121_... ./gen_bulk_tests CWE242 combo_file"
else
	for (( i=0; i<${#files[@]}; i++ )); do
		cat my_io.c $1/${files[$i]} > $3_${suffixes[$i]}
	done
fi
