#include <stdio.h>
int main(){
	int a[4] = {0x41424344, 0x45464748};
	char * b = (char *) a;
	short * c = a;	
	for(int i = 0; i < 8; i++)
		printf("%x ", *(b+i));
	printf("\n");
	for(int i = 0; i < 4; i++)
		printf("%x ", *(c+i));
	printf("\n");
	for(int i = 0; i < 2; i++)
		printf("%x ", *(a+i));
	printf("\n");
	b[0] = 0x49;
	for(int i = 0; i < 8; i++)
		printf("%x ", *(b+i));
	printf("\n");
	for(int i = 0; i < 2; i++)
		printf("%x ", *(a+i));
	printf("\n");
	b[1] = 0x4a;
	for(int i = 0; i < 8; i++)
		printf("%x ", *(b+i));
	printf("\n");
	for(int i = 0; i < 2; i++)
		printf("%x ", *(a+i));
	printf("\n");
	
	b[2] = 0x4b;
	for(int i = 0; i < 8; i++)
		printf("%x ", *(b+i));
	printf("\n");
	for(int i = 0; i < 2; i++)
		printf("%x ", *(a+i));
	printf("\n");
	return 0;
	

	/*
	int a[4] = {0x41424344, 0x45464748};
	
	for(int i = 0; i < 2; i++)
		printf("%x ", *(a+i));
	printf("\n");
	char * b = (char *)a;
	for(int i = 0; i < 8; i++)
		printf("%c ", *(b+i));
	printf("\n");
	short * c = (short *)a;
	for(int i = 0; i <4; i++)
		printf("%x ", *(c+i));
	printf("\n");
	c[0] = 0x494a;
	for(int i = 0; i <4; i++)
		printf("%x ", *(c+i));
	printf("\n");

	for(int i = 0; i < 2; i++)
		printf("%x ", *(a+i));
	printf("\n");
	c[1] = 0x4b4c;
	for(int i = 0; i <4; i++)
		printf("%x ", *(c+i));
	printf("\n");

	for(int i = 0; i < 2; i++)
		printf("%x ", *(a+i));
	printf("\n");

	for(int i = 0; i < 8; i++)
		printf("%x ", *(b+i));
	printf("\n");
	*/

	/* short b[4] = {0x1122, 0x3344, 0x5566, 0x7788}; */
	/* printf("4 shorts: "); */
	/* for(int i = 0; i <4; i++) */
	/* 	printf("%x ", *(b+i)); */
	/* printf("\n"); */
	/* int * c = (int *) b; */

	/* printf("2 ints: "); */
	/* for(int i = 0; i <2; i++) */
	/* 	printf("%x ", *(c+i)); */
	/* printf("\n"); */
	
	/* c[0] = 0x41424344; */
	/* printf("4 shorts: "); */
	/* for(int i = 0; i <4; i++) */
	/* 	printf("%x ", *(b+i)); */
	/* printf("\n"); */

	/* printf("2 ints: "); */
	/* for(int i = 0; i <2; i++) */
	/* 	printf("%x ", *(c+i)); */
	/* printf("\n"); */

	/* char * s = "hello"; */
	/* int * x = s+3; */
	/* printf("%x\n", *x); */

}
