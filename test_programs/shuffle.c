/* TREVOR PEITZMAN
 * Your actual code should start below.
 * switch statement syntax refreshed by
 * https://www.geeksforgeeks.org/switch-statement-cc/
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Shuffles and returns a deck of cards as an array of ints
int* shuffle(int seed);

// Simple fucntion to print the deck to stdout after decoding
// the cardindex values into suit and facevalue
void printdeck(int* deck);

int main() {

  // short and sweet. get the seed, shuffle, print deck.
  int seed;
  printf("Seed: ");
  scanf("%d", &seed);
  int* deck = shuffle(seed);
  printdeck(deck);

  return 0;
}

int* shuffle(int seed){
  // establish array for the deck
  int* deck = calloc(52, sizeof(int));
  int suitnumber = 1, facevalue;
  for (int i = 0; i < 52; i++) {
    if (i % 13 == 0 && i != 0) {
      suitnumber++;
      facevalue = 2;
    }
    facevalue = 2 + i % 13;// determine when the suit should increase
    // encode the facevalue and suitnumber in cardindex format
    deck[i] = 100 * suitnumber + facevalue;
  }

  // if selected seed is 0, print an ordered (nonshuffled) deck
  if (seed != 0) {
    srand(seed);
    for (int i = 51; i >= 0; i--) {
      int j = rand() % (i + 1);
      int temp = deck[i];
      deck[i] = deck[j];
      deck[j] = temp;
    }
  }
  return deck;
}

void printdeck(int* deck){
  int suitnumber, facevalue;
  char CLUB[]    = "\u2663"; // ♣
  char DIAMOND[] = "\u2666"; // ♦
  char HEART[]   = "\u2665"; // ♥
  char SPADE[]   = "\u2660"; // ♠

  // decode cardindex into suitnumber and facevalue for all cards in the deck
  for (int i = 0; i < 52; i++) {
    suitnumber = deck[i] / 100;  // integer division rounds down!
    facevalue = deck[i] % 100;

    // print the correct facevalue, adjusted to chars when necessary
    switch (facevalue) {
      case 11:
        printf(" J");
        break;
      case 12:
        printf(" Q");
        break;
      case 13:
        printf(" K");
        break;
      case 14:
        printf(" A");
        break;
      default:
        printf("%2d", facevalue);
        break;
    }

    // print the proper suit character depending on the suitnumber
    switch (suitnumber) {
      case 1:
        printf("%s\n", CLUB);
        break;
      case 2:
        printf("%s\n", DIAMOND);
        break;
      case 3:
        printf("%s\n", HEART);
        break;
      case 4:
        printf("%s\n", SPADE);
        break;
      default:
        printf("ERROR!\n");
        break;
    }
  }
}
