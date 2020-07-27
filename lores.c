#include "stdio.h"
#include "defs.h"

int main() {
    allInit();

    U64 bb = 0ULL;

    printf("Start\n");
    printBitboard(bb);

    printf("Start\n");
    bb = bb | (1ULL << SQ64(D2));             //add pawn on d2
    bb = bb | (1ULL << SQ64(G2));
    printBitboard(bb);




    return 0;
}
