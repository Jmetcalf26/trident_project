

#include <stdio.h>
#include <string.h>
int main() {  
    int berthing[2];
    char name[8];
    printf("Enter your wing and deck: ");
    scanf(" %d %d", berthing, berthing+1);
    printf("Enter your name: ");
    scanf("%s", name);  
    printf("%s lives in %d wing and on %d deck\n", 
										name, berthing[0], berthing[1]);
    
    return 0;
}



