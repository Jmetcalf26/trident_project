// TREVOR PEITZMAN
// You should NOT edit the main() function below

#include <stdio.h>

// YOUR TASK: Add the prototype and definition for the
// split function that makes the program work.
void split(double amt, int* dollars, int* cents);

int main() {
  /* DON'T CHANGE MAIN! Just write a good split() function
   * prototype and definition above and below.
   */
  printf("Enter amount: ");
  fflush(stdout);

  double amt;
  if (scanf(" $%lg", &amt) != 1) {
    printf("ERROR: must enter something like $3.50\n");
    return 1;
  }

  // Function Call Here!
  int dollars;
  int cents;
  split(amt, &dollars, &cents);

  printf("That's %i dollars and %i cents.\n", dollars, cents);

  return 0;
}

void split(double amt, int* dollars, int* cents){
  *dollars = (int)amt;
  *cents = (amt - *dollars) * 100;
}
