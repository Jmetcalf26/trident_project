#include <stdio.h>
int main(){
				char c[] = {'A', 'B', 'C', 'D'};
				char * d = &c;
				printf("%c\n", *d);
				int * e = &c;
				printf("%x\n", *e);
}
