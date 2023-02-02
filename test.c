// Another example program to demonstrate working
// of enum in C

int foo(char);
int bar(char c){

}
int (*bazz) (char) = bar;
int main(){

	foo('c');
	bar('c');
	bazz('c');
	bingo('c');
	bazz = bar;
}


