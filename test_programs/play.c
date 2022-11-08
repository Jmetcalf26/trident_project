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
int printcard(int cardindex, int* score);

// Combined implementer of printcard - will display both the user and Dealer
// hands in the proper format. "hide" makes the 2nd dealer card "**"
void printhands(int* player, int* dealer, int hide, int* pscore, int* dscore);

// Places a single card of format "cardindex" from the top of the deck into
// the next open slot in the given array "hand"
void deal(int* hand, int* deck, int* deckpos);

// the master function - calls all others in the proper order, handles scores,
// determines the winner, and allows for "rematches" when necessary
void play(int seed);

int main() {
  // keep main simple: establish seed and srand, call play to begin game.
  int seed;
  printf("Seed: ");
  scanf("%d", &seed);
  srand(seed);
  play(seed);

  return 0;
}

void play(int seed){
  // establish necessary deck and hands for single-player game
  int* deck = shuffle(seed);
  int player[52] = { 0 };
  int dealer[52] = { 0 };
  int deckpos = 51, sleeptime = 2, pscore = 0, dscore = 0;
  char cmd = 'h'; //usr's decision to hit or stand
  int pbust =0, dbust =0;

  // deal the initial two cards to each player
  for (int i = 0; i < 2; i++) {
    deal(player, deck, &deckpos);
    deal(dealer, deck, &deckpos);
  }

  // The "Player Interaction" Loop
  while (cmd == 'h' && pscore <= 21){
    printhands(player, dealer, 1, &pscore, &dscore);
    //allow to keep playing if not busted
    if (pscore <= 21) {
      printf("Hit or stand? [h/s] ");
      scanf(" %c", &cmd);
      if (cmd == 'h') 
        deal(player, deck, &deckpos);
      
    } else {
      printf("Player busts!\n");
      pbust =1;
      break;
    }
  }

  // Where the dealer magic happens
  while (dscore <= 21){
    printhands(player, dealer, 0, &pscore, &dscore);
    sleep(sleeptime);
    // These implement the "dealer rules"
    if (pbust || (dscore >= 17 && dscore <= 21)) {
      printf("Dealer stands.\n");
      break;
    } else if (dscore > 21) {
      printf("Dealer busts!\n");
      dbust =1;
    } else {
      printf("Dealer hits.\n");
      deal(dealer, deck, &deckpos);
    }
  }


  // print final results
  printf("\nFinal scores: Player %d, Dealer %d.\n", pscore, dscore);
  // push when tie
  if (pscore == dscore) {
    printf("Push! Play again.\n");
    play(seed);
  } else if (pbust || (!dbust && dscore > pscore)) {
    // Dealer wins if player busted or the dealer hasn't busted and
    // the dealer score is greater than the player score
    printf("Dealer wins!\n");
  } else {
    printf("Player wins!\n");
  }
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

void printhands(int* player, int* dealer, int hide, int* pscore, int* dscore) {
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

  // reset the score every time the hands are printed
  *pscore = 0;
  *dscore = 0;

  // print out the hands in the proper fashion
  printf("\n Player Dealer\n");
  for (int i = 0; i < max; i++) {
    printf("| ");
    if (player[i] != '\0') {
      *pscore = printcard(player[i], pscore);
    } else {
      printf("    ");
    }
    printf(" | ");
    if (dealer[i] != '\0') {
      // obfuscate the dealer's second card if its still the player's turn
      if (i == 1 && hide) {
        printf(" ** ");
      } else {
        *dscore = printcard(dealer[i], dscore);
      }
    } else {
      printf("    ");
    }
    printf(" |\n");
  }
}

int* shuffle(int seed){
  // establish array for the deck
  int deck[52] = { 0 };
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
    for (int i = 51; i >= 0; i--) {
      int j = rand() % (i + 1);
      int temp = deck[i];
      deck[i] = deck[j];
      deck[j] = temp;
    }
  }
  return deck;
}

int printcard(int cardindex, int* score){

  // decode cardindex into suitnumber and facevalue
  int suitnumber = cardindex / 100;  // integer division rounds down!
  int facevalue = cardindex % 100;

  // print the correct facevalue, adjusted to chars when necessary
  switch (facevalue) {
    case 11:
      printf(" J");
      *score += 10;
      break;
    case 12:
      printf(" Q");
      *score += 10;
      break;
    case 13:
      printf(" K");
      *score += 10;
      break;
    case 14:
      printf(" A");
      // logic for handling multiple Aces in a row, and the adjustment of value
      if (*score + 11 > 21 || *score == 2) {
        *score += 1;
        if (*score == 12) {
          *score = *score - 10;
        }
      } else {
        *score += 11;
      }
      break;
    default:
      printf("%2d", facevalue);
      *score += facevalue;
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
  return *score;
}

