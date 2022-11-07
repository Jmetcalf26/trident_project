/* TREVOR PEITZMAN
 * Your actual code should start below.
 * switch statement syntax refreshed by
 * https://www.geeksforgeeks.org/switch-statement-cc/
 * ternary operator refreshed by https://en.wikipedia.org/wiki/%3F:
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Shuffles and returns a deck of cards as an array of ints
int* shuffle(int seed);

// takes in a "cardindex" from the deck array and prints it while incrementing
// the score.
void printcard(int cardindex);

// Combined implementer of printcard - will display both the user and Dealer
// hands in the proper format. "hide" makes the 2nd dealer card "**"
void printhands(int* player, int* dealer);

// Places a single card of format "cardindex" from the top of the deck into
// the next open slot in the given array "hand"
void deal(int* hand, int* deck, int* deckpos);

// the master function - calls all others in the proper order, handles scores,
// determines the winner, and allows for "rematches" when necessary
void play(int* deck);

int main() {
  // keep main simple: establish seed and srand, call play to begin game.
  int seed;
  printf("Seed: ");
  scanf("%d", &seed);
  int* deck = shuffle(seed);
  play(deck);

  free(deck);

  return 0;
}

void play(int* deck){
  // establish necessary deck and hands for single-player game
  int* player = calloc(52, sizeof(int));
  int* dealer = calloc(52, sizeof(int));
  int deckpos = 51, sleeptime = 2;
  char cmd; //usr's decision to hit or stand

  // deal the initial two cards to each player
  for (int i = 0; i < 2; i++) {
    deal(player, deck, &deckpos);
    deal(dealer, deck, &deckpos);
  }

  printhands(player, dealer);
  printf("Hit or stand? [h/s] ");
  scanf(" %c", &cmd);

  // Allow player to hit as much as they want
  while (cmd == 'h'){
    deal(player, deck, &deckpos);
    printhands(player, dealer);
    printf("Hit or stand? [h/s] ");
    scanf(" %c", &cmd);
  }

  // Default 2 dealer hits
  for (int i = 0; i < 2; i++) {
    printhands(player, dealer);
    sleep(sleeptime);
    printf("Dealer hits.\n");
    deal(dealer, deck, &deckpos);
  }

  printhands(player, dealer);
  sleep(sleeptime);
  printf("Dealer stands.\n");

  free(player);
  free(dealer);

}

void deal(int* hand, int* deck, int* deckpos){
  int handpos = 0;
  // increment handpos until an empty position is found
  while (hand[handpos] != '\0') {
    handpos++;
  }
  // insert card from top of deck into next open slot in array hand
  hand[handpos] = deck[*deckpos];
  // decrement the deckposition
  *deckpos -= 1;
}

void printhands(int* player, int* dealer) {
  printf("\n Player Dealer\n");
  // find out whether the dealer or the player has more cards in their hand
  int max = 0, dealmax = 0;
  while (player[max] != '\0') {
    max++;
  }
  while (dealer[dealmax] != '\0') {
    dealmax++;
  }
  // if dealmax is greater than max, set max = dealmax, else leave max alone
  dealmax > max ? max = dealmax : max;

  // print out the hands in the proper fashion
  for (int i = 0; i < max; i++) {
    printf("| ");
    if (player[i] != '\0') {
      printcard(player[i]);
    } else {
      printf("    ");
    }
    printf(" | ");
    if (dealer[i] != '\0') {
      printcard(dealer[i]);
    } else {
      printf("    ");
    }
    printf(" |\n");
  }
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
    facevalue = 2 + i % 13; // determine when the suit should increase
    // encode the facevalue and suitnumber in cardindex format
    deck[i] = 100 * suitnumber + facevalue;
  }

  // if selected seed is 0, print an ordered deck
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

void printcard(int cardindex){

  // print the correct facevalue, adjusted to chars when necessary
  int suitnumber = cardindex / 100;  // integer division rounds down!
  int facevalue = cardindex % 100;

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
      printf("\u2663 ");
      break;
    case 2:
      printf("\u2666 ");
      break;
    case 3:
      printf("\u2665 ");
      break;
    case 4:
      printf("\u2660 ");
      break;
    default:
      printf("ERROR! ");
      break;
  }

}
