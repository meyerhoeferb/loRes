#include "stdio.h"
#include "defs.h"

int main() {
    allInit();

    S_BOARD board[1];

    parseFen(START_FEN, board);
    printBoard(board);

    parseFen("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1", board);
    printBoard(board);

    parseFen("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2", board);
    printBoard(board);

    parseFen("rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2", board);
    printBoard(board);

    return 0;
}
