#include <stdio.h>

#include <string.h>
int main(){
	int a[5] = {1, 2, 3, 4, 5};
	int b = 3;
	int *c = &b;
	int i =0;
	while(a[i] != 4){
		i++;
	}
	a[i] = a[*c];

	*c -= 1;

}

