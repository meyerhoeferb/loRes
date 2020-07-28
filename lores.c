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


    return 0;
}
