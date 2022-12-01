#include <stdio.h>
#include <stdlib.h>
int main(){
	char * a = malloc(4);
	a[2] = 0x41;
	for(int i =0; i < 4; i++)
		printf("%d\n", a[i]);
	for(int i = 0; i < 5; i++)
		continue;
	free(a);
}

