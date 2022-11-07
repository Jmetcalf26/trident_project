/* TREVOR PEITZMAN
 * Your actual code should start below.
 */

// Convert each 'a' to '@'
// Convert each 'e' to '3'
// Convert each 'i' to '!'
// Convert each 't' to '+'

#include <stdio.h>
#include <string.h>

int replacements(char* word);

int main() {

  int length, best = 0;
  char curr_word[128], best_word[128];

  while (strcmp(curr_word, "DONE")) {
    scanf("%s", curr_word);
    int curr = replacements(curr_word);
    printf("%s\n", curr_word);
    if (curr > best) {
      strcpy(best_word, curr_word);
      best = curr;
    }
  }

  printf("%d conversions for \"%s\"\n", best, best_word);

  return 0;
}

int replacements(char* word){
  int replacements = 0;

  for (int i = 0; word[i] != 0; i++) {
    if (word[i] == 'a') {
      word[i] = '@';
      replacements++;
    } else if (word[i] == 'e') {
      word[i] = '3';
      replacements++;
    } else if (word[i] == 'i') {
      word[i] = '!';
      replacements++;
    } else if (word[i] == 't') {
      word[i] = '+';
      replacements++;
    }
  }

  return replacements;
}
