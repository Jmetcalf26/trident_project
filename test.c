// Another example program to demonstrate working
// of enum in C
#include<stdio.h>

enum year{Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec};
enum State {Working = 1, Failed = 0, Freezed = 0};
enum Stat {Work = -1, Fail, Dunder = 4, Booga, Freeze = 0, Briggus};

int main(){
	printf("%d\n", Work);
	printf("%d\n", Fail);
	printf("%d\n", Dunder);
	printf("%d\n", Booga);
	printf("%d\n", Freeze);
	printf("%d\n", Briggus);
	enum year i;
	for (i=Jan; i<=Dec; i++)	
		printf("%d ", i);
	int Dunder = 1;		
	printf("\n%d\n", Dunder);
	return 0;

}


