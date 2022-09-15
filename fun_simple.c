#include <stdio.h>
int main(){
	int a = 10;
	int * b = &a;
	int d = *b;
	int c[2] = {1, 3};
  d = *(c+1);
	printf("%d\n", d);
	return 10;
}


