#include "stdio.h"
#include "defs.h"


int main() {
    allInit();

    S_BOARD board[1];

    parseFen(TEST_FEN, board);
    checkBoard(board);
    printBoard(board);
    printBitboard(board->pawns[WHITE]);
    printBitboard(board->pawns[BLACK]);
    printBitboard(board->pawns[BOTH]);
    showSqAtkBySide(WHITE, board);
    showSqAtkBySide(BLACK, board);


    int move = 0;
    int from = 6; int to = 12; int captured = wR; int promoted = bR;
    move = (from) | (to << 7) | (captured << 14) | (promoted << 20);

    printf("\ndec:%d hex%X\n", move, move);

    printf("from: %d to: %d cap: %d prom: %d\n", FROMSQ(move), TOSQ(move), CAPTURED(move), PROMOTED(move));

    return 0;
}
