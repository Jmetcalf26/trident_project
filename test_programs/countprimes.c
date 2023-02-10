/* Trevor Peitzman
 * Your actual code should start below.
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int getnum(int atleast);
int countprimes(int a, int b);
bool isprime(int n);

int main() {

  int a = getnum(1);
  int b = getnum(a);
  printf("There are %d primes between %d and %d.\n", countprimes(a, b), a, b);

  return 0;
}

// Reads a single number from the terminal that is at least
// as large as the given integer.
// If the user enters a number too small, they will repeatedly
// be prompted again and again until they enter a number that
// is large enough.
int getnum(int atleast){
  int in;
  printf("Enter a number at least %d: ", atleast);
  scanf("%i", &in);
  if (in < atleast) {
    printf("Too small!\n");
    in = getnum(atleast);
  }
  return in;
}

// Returns the number of primes between a and b.
// The count is inclusive meaning that if a or b is a prime,
// they should be included in the count.
int countprimes(int a, int b){
  int total = 0;
  if (a == b) {
    if (isprime(a)) {
      total++;
    }
  } else if (isprime(a)) {
    total++;
    total += countprimes(a + 1, b);
  } else {
    total = countprimes(a + 1, b);
  }
  return total;
}

// Determines whether n is a prime number.
// If it is, true is returned, and if not, false is returned.
bool isprime(int n) {
  if (n < 2) {
    // 2 is the smallest prime.
    return false;
  }

  // try all possible divisors of n
  for (int fact=2; fact*fact <= n; ++fact) {
    if (n % fact == 0) {
      // n is divisible by fact, so not a prime
      return false;
    }
  }

  // n doesn't have ANY factors, so it's a prime.
  return true;
}
