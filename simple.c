#include <stdio.h>

#include <string.h>
int main(){
	char a[12];
	scanf("%s", a);
	printf("%s\n", a);
	char b[12];
	strcpy(b, a);
	printf("%s", b);
	return 0;

}

