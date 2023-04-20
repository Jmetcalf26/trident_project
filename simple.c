

#include <stdio.h>
#include <stdlib.h>

int main(){
  int x = 3;
  int * y = &x;
  x = 6;
  printf("%d\n", x);
  *y = 5;
  printf("%d\n", x);
  y[0] = 7;
  printf("%d\n", x);
  int z = x + *y + y[0];
  printf("%d\n", z);
  return 0;
}







