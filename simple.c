#include <stdio.h>
int main(){
	int a[] = {1, 2, 3};
	char * b = (char *) a;
	b[5] = 3;
	puts(a[1]);
	return 0;
}
