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
}
