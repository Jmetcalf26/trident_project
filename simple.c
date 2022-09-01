//#include <stdio.h>
int booga(int a){
	
	int b = -a;
	while(b > 0){
		a = a + 1;
		a = a - 1;
	}
	else
		a = a + 1;
	if(b == 0){
		a = a + 3;
	}
	else
					a = a + 2;
	/* printf("%d\n", b); */
	return a^1;
}
int main(){
	int a = 1;
	return booga(a);
}


