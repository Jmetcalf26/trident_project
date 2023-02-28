#include <stdio.h>

typedef int NAME;

struct booga{
  int i;
  char c;

};

typedef struct{
  int i;
  char c;
}bringus;

struct booga foo(){
  struct booga a = {2, 'b'};
  return a; 
}

int main(){
  NAME chuck[] = {1, 3, 4 };
  struct booga d = foo();
  bringus f = {1, 'A'};
  printf("%x\n", d);
  printf("%x\n", foo());
  printf("%x\n", foo());

  int e = foo().i;
  //foo().a = 3;
  NAME jack[5] = {1, 2 };
  NAME dan[] = {1, 2, 3};
  struct booga a = {1, 'a'};
  struct booga* c = &a;
  int b = a.i;
  printf("%c\n", a.c);
  printf("%c\n", c->c);
  printf("%d\n", b);
}
