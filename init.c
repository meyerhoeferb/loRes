
#include "defs.h"
#include "stdlib.h"

//generate random 64 bit number, rand makes 15 bit number so add a bunch of them together shifted over
//last line just takes the 4 final bits we need to fill 64
#define RAND64 (    (U64)rand() | \
                    ((U64)rand() << 15) | \
                    ((U64)rand() << 30) | \
                    ((U64)rand() << 45) | \
                    (((U64)rand() & 0xf) << 60) )


int sq120ToSq64[BRD_SQ_NUM];
int sq64ToSq120[64];

U64 setMask[64];
U64 clearMask[64];

U64 pieceKeys[13][120];             //these all hold random U64 numbers, used for hashing position
U64 sideKey;
U64 castleKeys[16];

int filesBrd[BRD_SQ_NUM];
int ranksBrd[BRD_SQ_NUM];

//set up rank and file arrays
void initRankFileArrays() {
    int i = 0;
    for(i = 0; i < BRD_SQ_NUM; i++) {
        filesBrd[i] = NO_SQ;
        ranksBrd[i] = NO_SQ;
    }

    int rank = RANK_1;
    int file = FILE_A;
    int sq = 0;
    for(rank = RANK_1; rank <= RANK_8; rank++) {
        for(file = FILE_A; file <= FILE_H; file++) {
            sq = FR2SQ(file, rank);
            filesBrd[sq] = file;
            ranksBrd[sq] = rank;
        }
    }
}

//set up arrays for position hashing
void initHashKeys() {
    int i = 0;
    int j = 0;
    for(i = 0; i < 13; i++) {
        for(j = 0; j < 120; j++) {
            pieceKeys[i][j] = RAND64;
        }
    }

    sideKey = RAND64;

    for(i = 0; i < 16; i++) {
        castleKeys[i] = RAND64;
    }
}

//setup arrays that allow us to quickly access the appropriate number to set or clear a bit given the 64base index
void initBitMasks() {
    int i = 0;

    for(i = 0; i < 64; i++) {
        setMask[i] = 0;
        clearMask[i] = 0;
    }

    for(i = 0; i < 64; i++) {
        setMask[i] = (1ULL << i);
        clearMask[i] = ~setMask[i];
    }

}

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
    initBitMasks();
    initHashKeys();
    return;
}
