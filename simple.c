#include <stdio.h>
int main(){
  int a[3] = {0x41424344, 0x45464748, 0x494a4b4c};
  for(int i = 0; i < 2; i++)
    printf("%d-", a[i]);
  printf("%d\n", a[2]);

  printf("IMPLICIT CAST TIME\n");
  char * d =  a;
  for(int i = 0; i < 11; i++)
    printf("%d-", d[i]);
  printf("%d\n", d[11]);

  printf("EXPLICIT CAST TIME\n");
  char * c = (char*) a;
  for(int i = 0; i < 11; i++)
    printf("%d-", c[i]);
  printf("%d\n", c[11]);

  printf("\n");
  

}
