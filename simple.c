#include <stdio.h>
int main(){
  /*int g[] = {1, 2};
  g[0] = 3;
  double test = 1.9;
  int e = 1;
  e = test + e;
  */
  int a = 0x11223344;
  int * b = &a;
  char * c =  b;
  short * d = b;
  printf("%c\n", c[0]);
  printf("%hi\n", *d);
  char * e = "heyy";
  printf("%d\n", e[0]);
  printf("%c\n", (char) e[0]);
  int f = 1.5;
  printf("%d\n", f);
  printf("%lf\n", f);
}
