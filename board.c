#include "stdio.h"
#include "defs.h"

//parse a fen and set up the position
int parseFen(char *fen, S_BOARD *pos) {
    ASSERT(fen != NULL);
    ASSERT(pos != NULL);

    int rank = RANK_8;
    int file = FILE_A;
    int piece = 0;
    int count = 0;
    int i = 0;
    int sq64 = 0;
    int sq120 = 0;

    resetBoard(pos);

    //this is disgusting and i hate it but technically it works (some of his code is so ugly)
    while ((rank >= RANK_1) && *fen) {
	    count = 1;
		switch (*fen) {
            case 'p': piece = bP; break;
            case 'r': piece = bR; break;
            case 'n': piece = bN; break;
            case 'b': piece = bB; break;
            case 'k': piece = bK; break;
            case 'q': piece = bQ; break;
            case 'P': piece = wP; break;
            case 'R': piece = wR; break;
            case 'N': piece = wN; break;
            case 'B': piece = wB; break;
            case 'K': piece = wK; break;
            case 'Q': piece = wQ; break;

            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
                piece = EMPTY;
                count = *fen - '0';
                break;

            case '/':
            case ' ':
                rank--;
                file = FILE_A;
                fen++;
                continue;

            default:
                printf("FEN error \n");
                return -1;
        }

		for (i = 0; i < count; i++) {
            sq64 = rank * 8 + file;
			sq120 = SQ120(sq64);
            if (piece != EMPTY) {
                pos->pieces[sq120] = piece;
            }
			file++;
        }
		fen++;
	}

    //turn
    ASSERT(*fen == 'w' || *fen == 'b');
    pos->side = (*fen == 'w') ? WHITE : BLACK;
    fen += 2;

    //castling permissions
    for(i = 0; i < 4; i++) {
        if(*fen == ' ') {
            break;
        }
        switch(*fen) {
            case 'K': pos->castlePerm |= WKCA; break;
            case 'Q': pos->castlePerm |= WQCA; break;
            case 'k': pos->castlePerm |= BKCA; break;
            case 'q': pos->castlePerm |= BQCA; break;
            default: break; //reading a dash just moves on to a space which gets out of the loop
        }
        fen++;
    }
    fen++;

    ASSERT(pos->castlePerm >= 0 && pos->castlePerm < 16);

    //en passant
    if(*fen != '-') {
        file = fen[0] - 'a';
        rank = fen[1] - '1';

        ASSERT(file >= FILE_A && file <= FILE_H);
        ASSERT(rank >= RANK_1 && rank <= RANK_8);

        pos->enPas = FR2SQ(file, rank);
    }

    //generate position hash
    pos->posKey = generatePosKey(pos);

    return 0;
}

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
        pos->pawns[i] = 0ULL;
    }
    for(i = 0; i < 2; i++) {
        pos->bigPc[i] = 0;
        pos->minPc[i] = 0;
        pos->majPc[i] = 0;
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

    //TODO: halfmove clock and total move count
}

//print the board
void printBoard(const S_BOARD *pos) {

    printf("Game Board: \n\n");

    int sq, file, rank, piece;
    for(rank = RANK_8; rank >= RANK_1; rank--) {
        printf("%d", rank + 1);
        for(file = FILE_A; file <= FILE_H; file++) {
            sq = FR2SQ(file, rank);
            piece = pos->pieces[sq];
            printf("%3s", pcChar[piece]);
        }
        printf("\n");
    }
    printf(" ");
    for(file = FILE_A; file <= FILE_H; file++) {
        printf("%c", 'a' + file);
    }

    printf("\n");
    printf("side: %c\n", sideChar[pos->side]);
    printf("enPas: %d\n", pos->enPas);
    printf("castle: %c%c%c%c\n",
            pos->castlePerm & WKCA?'K':'-',
            pos->castlePerm & WQCA?'Q':'-',
            pos->castlePerm & BKCA?'k':'-',
            pos->castlePerm & BQCA?'q':'-');

    printf("Hash: %llX\n", pos->posKey);

}

//update piece lists
void updatePcLists(S_BOARD *pos) {
    int pc, sq, color, i;

    for(i = 0; i < BRD_SQ_NUM; i++) {
        sq = i;
        pc = pos->pieces[i];
        if(pc != NO_SQ && pc != EMPTY) {
            color = pcCol[pc];
            if(pcBig[pc]) pos->bigPc[color]++;
            if(pcMin[pc]) pos->minPc[color]++;
            if(pcMaj[pc]) pos->majPc[color]++;

            pos->material[color] += pcVal[pc];

            pos->pcList[pc][pos->pcNum[pc]] = sq;
            pos->pcNum[pc]++;

            if(pc == wK || pc == bK) pos->kingSq[color] = sq;

        }
    }
}
