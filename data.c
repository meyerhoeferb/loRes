#include "defs.h"

// for printing
char *pcChar[13] = {"\u25FB", "\u265F", "\u265E", "\u265D", "\u265C", "\u265B",
        "\u265A", "\u2659", "\u2658", "\u2657", "\u2656", "\u2655", "\u2654"};
char sideChar[] = "wb-";
char rankChar[] = "12345678";
char fileChar[] = "abcdefgh";

//easy lookup of piece attributes
int pcBig[13] = {FALSE, FALSE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, TRUE, TRUE, TRUE, TRUE, TRUE};
int pcMaj[13] = {FALSE, FALSE, FALSE, FALSE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, TRUE, TRUE, TRUE};
int pcMin[13] = {FALSE, FALSE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, TRUE, TRUE, FALSE, FALSE, FALSE};
int pcVal[13] = {0, 100, 325, 325, 550, 1000, 50000, 100, 325, 325, 550, 1000, 50000};
int pcCol[13] = {BOTH, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK};
