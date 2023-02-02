// Another example program to demonstrate working
// of enum in C
#include<stdio.h>

int main(){
  int i =0;
  int j = 0;
  i = 1;
  int * a = &i;
  a = &j;
  *a = 2;
  j = *a;
  int k[4] = {0, 1, 2};
  a = &k[2];
  printf("%d\n", i);
  printf("%x\n", a);
  printf("%d\n", j);
  printf("%d\n", j);
  printf("%d\n", *a);
}
