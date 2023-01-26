#include <stdio.h>
#include <stdlib.h>

int main(){
	int x[3] = {0, 1, 2};
	printf("%d\n", x[0]);
	printf("%d\n", x[1]);
	printf("%d\n", x[2]);
	int q = 1;	
	int r = 2;

	q = r;

	x[0] = 1;
	int  p= x[0] + x[|'a', type1];
	int * a = &x[0];
	int * b = &x[1];
	int * c = &x[2];
	printf("%x\n", a);
	printf("%x\n", b);
	printf("%x\n", c);
	
	printf("%x\n", &q);
	printf("%d\n", *a);
	printf("%d\n", *b);
	printf("%d\n", *c);

	int * d[3] = {a, b, c};
	printf("%x\n", d);
	printf("%x\n", d[0]);
	printf("%d\n", *d[0]);
	printf("%d\n", *d[1]);
	printf("%d\n", *d[2]);
}

