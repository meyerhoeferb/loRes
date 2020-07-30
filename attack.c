#include "defs.h"
#include "stdio.h"

const int nAtk[8] = {-8, -19, -21, -12, 8, 19, 21, 12};
const int rAtk[8] = {-1, -10, 1, 10};
const int bAtk[8] = {-9, -11, 9, 11};
const int kAtk[8] = {-9, -11, 9, 11, -1, -10, 1, 10};

//check if square is being attacked by given side
int sqAttacked(const int sq, const int side, const S_BOARD *pos) {
    int pc, i, tempSq, dir;

    //pawns
    if (side == WHITE) {
        if(pos->pieces[sq - 11] == wP || pos->pieces[sq - 9] == wP) {
            return TRUE;
        }
    }else {
        if(pos->pieces[sq + 11] == bP || pos->pieces[sq + 9] == bP) {
            return TRUE;
        }
    }

    //knights
    for(i = 0; i < 8; i++) {
        pc = pos->pieces[sq + nAtk[i]];
        if(ISN(pc) && pcCol[pc] == side) {
            return TRUE;
        }
    }

    //bishop or queen diag
    for(i = 0; i < 4; i++) {
        dir = bAtk[i];
        tempSq = sq + dir;
        pc = pos->pieces[tempSq];
        while(pc != NO_SQ) {
            if((ISB(pc) || ISQ(pc)) && pcCol[pc] == side) {
                return TRUE;
            }
            break;
        }
        tempSq += dir;
        pc = pos->pieces[tempSq];
    }

    //rook or queen straight
    for(i = 0; i < 4; i++) {
        dir = rAtk[i];
        tempSq = sq + dir;
        pc = pos->pieces[tempSq];
        while(pc != NO_SQ) {
            if((ISR(pc) || ISQ(pc)) && pcCol[pc] == side) {
                return TRUE;
            }
            break;
        }
        tempSq += dir;
        pc = pos->pieces[tempSq];
    }

    //king
    for(i = 0; i < 8; i++) {
        pc = pos->pieces[sq + kAtk[i]];
        if(ISK(pc) && pcCol[pc] == side) {
            return TRUE;
        }
    }

    return FALSE;
}

//print the squares attacked by a side
void showSqAtkBySide(const int side, const S_BOARD *pos) {
	int rank = 0;
	int file = 0;
	int sq = 0;

	printf("\n\nSquares attacked by: %c\n", sideChar[side]);
	for(rank = RANK_8; rank >= RANK_1; rank--) {
		for(file = FILE_A; file <= FILE_H; file++) {
			sq = FR2SQ(file, rank);
			if(sqAttacked(sq, side, pos) == TRUE) {
				printf("X");
			}
			else {
				printf("-");
			}
		}
		printf("\n");
	}
	printf("\n");
}
