#include <stdio.h>
int main(){
  int a = 0x11223344;
  int * b = &a;
  char * c = (char *) b;
  printf("%c\n", c[0]);
  printf("%c\n", (char) c[0]);
  char * d = "heyy";
  printf("%d\n", d[0]);
  printf("%c\n", (char) d[0]);
}
