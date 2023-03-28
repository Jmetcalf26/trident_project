mapfile -t suffixes < <(ls | grep $1 | rev | cut -d'_' -f1 | rev)
mapfile -t files < <(ls | grep $1)
if [ $# -ne 2 ]; then
	echo "Usage: ./gen_bulk_tests <input_prefix> <output_prefix>"
	echo "  Example: ./gen_bulk_tests CWE242 combo_file"
else
	for (( i=0; i<${#files[@]}; i++ )); do
		cat my_io.c ${files[$i]} > $2_${suffixes[$i]}
	done
fi
