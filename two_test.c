#include <stdio.h>
int main(){
	short a[4] = {0x4142, 0x4344, 0x4546, 0x4748};

	for(int i = 0; i < 4; i++)
		printf("%x ", *(a+i));
	printf("\n");
	char * b = (char *)a;
	for(int i = 0; i < 8; i++)
		printf("%c ", *(b+i));
	printf("\n");
	int * c = (int *)a;
	for(int i = 0; i < 2; i++)
		printf("%x ", *(c+i));
	printf("\n");

	char d[8] = {0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48};
	for(int i = 0; i < 8; i++)
		printf("%x ", *(d+i));
	printf("\n");
	short * e = (short *)d;
	for(int i = 0; i < 4; i++)
		printf("%x ", *(e+i));
	printf("\n");
	int * f = (int *)e;
	for(int i = 0; i < 2; i++)
		printf("%x ", *(f+i));
	printf("\n");

	return 0;
}
