#include <stdio.h>
#define INT_MAX 4
int main(){
	int a =1;
	int * b = &a;
	int c = INT_MAX - 2;
	char * d = (char *) &c;
	printf("%c\n", *d);
	//int * d = &c;
	int e = *d;
	printf("%d %d %d\n", a, c, e);
}
