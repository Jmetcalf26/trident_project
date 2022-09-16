#include <stdio.h>
#include <stdlib.h>
int main(){
	int a[] = {1, 3};
	int * a2 = a+1;
	printf("A AS A POINTER: %p\n", a);
	printf("A AS A POINTER: %p\n", a2);
	printf("ADDR OF A: %p\n", &a);
	int * b = malloc(8);
	printf("B AS A POINTER: %p\n", b);
	printf("ADDR OF B: %p\n", &b);
	for(int i =0; i < 2; i++)
					printf("%d\n", a[i]);
	
	for(int i =0; i < 2; i++)
					printf("%d\n", b[i]);
	return 0;
}


