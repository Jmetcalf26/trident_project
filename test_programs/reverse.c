/* TREVOR PEITZMAN
 * Your actual code should start below.
 */

 #include <stdio.h>

int main() {

  int max = 0;
  printf("How many numbers? ");
  scanf("%d", &max);
  printf("Enter %d numbers: ", max);
  int nums[max];

  for (int i = 0; i < max; i++) {
    scanf(" %d", &nums[i]);
  }

  for (int i = max - 1; i >= 0; i--) {
    printf("%d\n", nums[i]);
  }

  return 0;
}
