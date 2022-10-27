#include <stdio.h>
int main(){
	int a[4] = {0x41424344, 0x45464748, 0x41414141, 0x41414141};
	
	for(int i = 0; i < 4; i++)
		printf("%x ", *(a+i));
	printf("\n");
	char * b = (char *)a;
	for(int i = 0; i < 16; i++)
		printf("%c ", *(b+i));
	printf("\n");
	short * c = (short *)a;
	for(int i = 0; i <8; i++)
		printf("%x ", *(c+i));
	printf("\n");
	c[0] = 0x494a;
	for(int i = 0; i <8; i++)
		printf("%x ", *(c+i));
	printf("\n");

	for(int i = 0; i < 4; i++)
		printf("%x ", *(a+i));
	printf("\n");

	for(int i = 0; i < 16; i++)
		printf("%x ", *(b+i));
	printf("\n");
	return 0;
}
