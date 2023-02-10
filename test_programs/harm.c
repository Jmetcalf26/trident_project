// Replace this comment with your name
// You should NOT edit the main() function below

#include <stdio.h>

// I want a function harm(n) that computes the nth harminic number, which
// is 1/1 + 1/2 + 1/3 + ... + 1/n.  Can you make it for me?
// Add the prototype and definition to this file that makes the program work.

double harm(int i);

int main() {
  /* DON'T CHANGE MAIN! Just write a good harm() function
   * prototype and definition above and below.
   */
  double target;
  printf("Enter target: ");
  fflush(stdout);
  scanf(" %lg", &target);

  double curharm = 0;
  int i = 0;
  do {
    i++;
    curharm = harm(i); //-- here's where I use harm!
  } while(curharm < target);

  printf("The %ith harmonic number is %g,"
         " which is the first greater than %g.\n",
         i, curharm, target);

  return 0;
}

double harm(int i){
  double out = 0;
  for (int counter = 1; counter <= i; counter++) {
    out += (1 / (double)counter);
  }
  return out;
}
