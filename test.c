#include <stdio.h>
int main(){
	int a[4] = {0x41424344, 0x45464748, 0x41414141, 0x41414141};
	char * b = (char *)a;
	for(int i = 0; i < 16; i++)
		printf("%c ", *(b+i));
	printf("\n");
	double * c = (double *)a;
	for(int i = 0; i < 2; i++)
		printf("%lf ", *(c+i));

	return 0;
}
