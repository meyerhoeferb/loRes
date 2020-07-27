#include "stdio.h"
#include "defs.h"

//remove all pieces, set all values to zero
void resetBoard(S_BOARD *pos) {
    int i = 0;

    //board state
    for(i = 0; i < BRD_SQ_NUM; i++) {
        pos->pieces[i] = NO_SQ;
    }
    //set actual board to empty
    for(i = 0; i < 64; i++) {
        pos->pieces[SQ120(i)] = EMPTY;
    }

    //clear piece lists and pawn bitboards
    for(i = 0; i < 3; i++) {
        pos->bigPc[i] = 0;
        pos->minPc[i] = 0;
        pos->majPc[i] = 0;
        pos->pawns[i] = 0ULL;
    }
    for(i = 0; i < 13; i++) {
        pos->pcNum[i] = 0;
    }

    //king squares
    pos->kingSq[WHITE] = pos->kingSq[BLACK] = NO_SQ;

    //side,enpas, fifty,plys, castling, hash
    pos->side = BOTH;
    pos->enPas = NO_SQ;
    pos->fiftyMove = 0;
    pos->ply = 0;
    pos->hisPly = 0;
    pos->castlePerm = 0;
    pos->posKey = 0ULL;



}
