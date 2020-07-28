#include "defs.h"
#include "stdio.h"

U64 generatePosKey(const S_BOARD *pos) {
    int sq = 0;
    U64 finalKey = 0;
    int piece = EMPTY;

    //hash in all pieces on board
    for(sq = 0; sq < BRD_SQ_NUM; sq++) {
        piece = pos->pieces[sq];
        if(piece != NO_SQ && piece != EMPTY && piece != NO_SQ) {
            ASSERT(piece>=wP && piece<=bK);
            finalKey ^= pieceKeys[piece][sq];
        }
    }

    //if white's turn, hash in sideKey
    if(pos->side == WHITE) {
        finalKey ^= sideKey;
    }

    //if enpas square exists, hash it in
    int enPas =  pos->enPas;
    if( enPas != NO_SQ) {
        ASSERT( enPas >= 0 &&  enPas < BRD_SQ_NUM);
        finalKey ^= pieceKeys[EMPTY][enPas];
    }

    //hash in castle permissions
    int castlePerm = pos->castlePerm;
    ASSERT(castlePerm >= 0 && castlePerm < 16);
    finalKey ^= castleKeys[castlePerm];

    return finalKey;
}
