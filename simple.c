#define end_of_metadata_macros 10
#include <limits.h>
int main(){
	int a = INT_MAX;
	char b = 1;
	int c = a + b;
	unsigned d = 3;
	double e = 1.5;
	long f = 1.5;
	float g = 1.5;
	printf("%d%d\n", a, c);
}
