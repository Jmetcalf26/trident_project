

#include <stdio.h>
#include <stdlib.h>

int main(){

  char name[12];
  printf("Please enter your name: ");
  gets(name);

  int company;
  printf("Please enter your company: ");
  scanf("%d", &company);

  printf("Hello %s! ", name);

  if(company < 25)
    printf("Only %d companies away from the best one!\n", 25-company);
  else if(company > 25)
    printf("Only %d companies away from the best one!\n", company-25);
  else
    printf("GO BEARSHARKS!\n");

  return 0;
}







