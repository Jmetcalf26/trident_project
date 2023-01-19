int main(){
	int * x;
	x[x[0]] = *(&x[1] + 1);
}
