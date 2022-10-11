// TREVOR PEITZMAN

#include <stdio.h>

int dupes(double x, double y, double z);

int main() {

  int sames = 2;
  double x, y, z;

  while (sames > 1 ) {
    printf("Enter three distinct numbers: ");
    scanf("%lg %lg %lg", &x, &y, &z);
    sames = dupes(x, y, z);
    if (dupes(x, y, z) <= 1) {
      return(0);
    }
    printf("There were %d duplicates. Try again.\n", sames);
  }

  return 0;
}

int dupes(double x, double y, double z) {
  int sames = 1;
  if (x == y || y == z || x == z) {
    sames++;
    if (x == y && z == y) {
      sames++;
    }
  }
  return sames;
}
