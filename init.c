

#include "defs.h"

int sq120ToSq64[BRD_SQ_NUM];
int sq64ToSq120[64];

void initSq120To64() {
    int i = 0;
    int file = FILE_A;
    int rank = RANK_1;
    int sq = A1;
    int sq64 = 0;

    for(i = 0; i < BRD_SQ_NUM; i++) {
        sq120ToSq64[i] = 65;
    }

    for(i = 0; i < 64; i++) {
        sq64ToSq120[i] = 120;
    }

    for(rank = RANK_1; rank <= RANK_8; rank++){
        for(file = FILE_A; file <= FILE_H; file++) {
            sq = FR2SQ(file, rank);
            sq64ToSq120[sq64] = sq;
            sq120ToSq64[sq] = sq64;
            sq64++;
        }
    }
}

void allInit() {
    initSq120To64();
    return;
}
