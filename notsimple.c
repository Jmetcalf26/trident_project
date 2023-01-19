#include <stdio.h>
#include <stdlib.h>
int main(){
	int x[3] = {0, 1, 2};
	int * a = &x[0];
	printf("%d\n", a);
	int * b = &x[1];
	printf("%d\n", b);
	int * c = &x[2];
	printf("%d\n", c);
	int * m[3] = {a, b, c};
	printf("%d\n", m);
	int * p = m[2];
	printf("%d\n", p);
	int n = *p;
	printf("%d\n", n);
	int q = *(m[2]);
	printf("%d\n", q);
	int o = *a;
	printf("%d\n", o);
//	int * a = &x;
}

