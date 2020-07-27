#include "stdio.h"
#include "defs.h"

int main() {
    allInit();

    U64 bb = 0ULL;

    printf("Start\n");
    bb = bb | (1ULL << SQ64(D2));             //add pawn on d2
    bb = bb | (1ULL << SQ64(D3));
    bb = bb | (1ULL << SQ64(D4));
    printBitboard(bb);

    int count = CNT(bb);

    printf("%d\n", count);

    int index = POP(&bb);

    printf("index: %d\n", index);

    printBitboard(bb);




    return 0;
}
