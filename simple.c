#include <stdio.h>
int main(){
  char * t = "ballas";
  int sld= 1;
  printf("%d\n", sld);
  int a = 0x11223344;
  int g[] = {1, 2};
  g[0] = 3;
  double test = 1.9;
  int e = 1;
  e = test + e;
  int * b = &a;
  char * c =  b;
  printf("%c\n", c[0]);
  printf("%c\n", (char) c[0]);
  char * d = "heyy";
  printf("%d\n", d[0]);
  printf("%c\n", (char) d[0]);
  int f = 1.5;
}
