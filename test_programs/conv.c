// TREVOR PEITZMAN
// You should only need to edit the main() function below.

#include <stdio.h>
#include <string.h>

//typedef char cstring[128];

// lenUnitCF(fromUnit,toUnit) - this function returns
// conversion factors between different units of length
// for units it understands, and returns 0.0 for units
// it does not understand.
// It understands: feet, inches, yards, miles, millimeters,
// centimeters, meters, kilometers, nautical-miles and light-years.
double lenUnitCF(char * fromUnit, char * toUnit);

double toFeet(char * fromUnit); // This just helps with lenUnitCF

int main() {

  char src[128];
  char dest[128];
  double amt;

  printf("convert: ");
  scanf("%lg", &amt);
  printf("from: ");
  scanf("%s", src);
  printf("to: ");
  scanf("%s", dest);
  printf("%g %s\n", amt * lenUnitCF(src, dest), dest);

  return 0;
}

/*** Don't change this function - just use it! */
double lenUnitCF(char * fromUnit, char * toUnit) {
  return toFeet(fromUnit)/toFeet(toUnit);
}

/*** Don't change this function - just use it! */
double toFeet(char * fromUnit) {
  if (strcmp(fromUnit, "feet") == 0) {
    return 1.0;
  } else if (strcmp(fromUnit, "inches") == 0) {
    return 1.0/12.0;
  } else if (strcmp(fromUnit, "yards") == 0) {
    return 3.0;
  } else if (strcmp(fromUnit, "miles") == 0) {
    return 5280;
  } else if (strcmp(fromUnit, "millimeters") == 0) {
    return 0.00328084;
  } else if (strcmp(fromUnit, "centimeters") == 0) {
    return 0.0328084;
  } else if (strcmp(fromUnit, "meters") == 0) {
    return 3.28084;
  } else if (strcmp(fromUnit, "kilometers") == 0) {
    return 3280.84;
  } else if (strcmp(fromUnit, "nautical-miles") == 0) {
    return 6076.12;
  } else if (strcmp(fromUnit, "light-years") == 0) {
    return 3.1038479e16;
  } else {
    return 0.0;
  }
}
