#ifndef DEFS_H
#define DEFS_H

#include "stdlib.h"

#define DEBUG

#ifndef DEBUG
#define ASSERT(n)

#else
#define ASSERT(n) \
if(!(n)) { \
printf("\nFAILED:  %s  ", #n); \
printf("In file %s ", __FILE__); \
printf("at line %d \n", __LINE__); \
exit(1);}
#endif

typedef unsigned long long U64;

#define NAME "loRes 1.0"
#define BRD_SQ_NUM 120

#define MAX_GAME_MOVES 2048        //max allowed half moves in a game

#define START_FEN "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#define TEST_FEN "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"


enum {EMPTY, wP, wN, wB, wR, wQ, wK, bP, bN, bB, bR, bQ, bK}; //piecetypes
enum {FILE_A, FILE_B, FILE_C, FILE_D, FILE_E, FILE_F, FILE_G, FILE_H, FILE_NONE};  //file and row translations
enum {RANK_1, RANK_2, RANK_3, RANK_4, RANK_5, RANK_6, RANK_7, RANK_8, RANK_NONE};
enum {WHITE, BLACK, BOTH};  //piece colors
enum {A1 = 21, B1, C1, D1, E1, F1, G1, H1,
      A2 = 31, B2, C2, D2, E2, F2, G2, H2,
      A3 = 41, B3, C3, D3, E3, F3, G3, H3,
      A4 = 51, B4, C4, D4, E4, F4, G4, H4,
      A5 = 61, B5, C5, D5, E5, F5, G5, H5,
      A6 = 76, B6, C6, D6, E6, F6, G6, H6,
      A7 = 81, B7, C7, D7, E7, F7, G7, H7,
      A8 = 91, B8, C8, D8, E8, F8, G8, H8, NO_SQ        //chess coord to array index
};

enum {FALSE, TRUE};      //boolean

enum {WKCA = 1, WQCA = 2, BKCA = 4, BQCA = 8};          //set bits for castling permissions

//undo move structure
typedef struct{
    int move;       //move played
    int castlePerm; //permissions before move
    int enPas;      //enpas before move
    int fiftyMove;  //count before move
    U64 posKey;     //hash of position prior to move
} S_UNDO;

//board structure
typedef struct {
    int pieces[BRD_SQ_NUM];     //board state
    U64 pawns[3];               //pawn bitboards (white,black,both)

    int kingSq[2];              //position of each king

    int side;                   //whose turn is it
    int enPas;                  //enpas square
    int fiftyMove;              //number of moves without pawn move/capture for draw condition

    int ply;                    //number of halfmoves in current search
    int hisPly;                 //number of halfmoves since engine start
    int totPly;                 //number of total half moves in game

    int castlePerm;             //castling permissions

    U64 posKey;                 //hash of position (for repitition)

    int pcNum[13];              //count of pieces on board
    int bigPc[2];               //count of nonpawns on board (white black both)
    int majPc[2];               //count of major pieces on board
    int minPc[2];               //count of minor pieces on board
    int material[2];            //sum of piece values for each side

    int pcList[13][10];          //piecelists for each type of piece (can possibly have 10 of each) makes movegen faster

    S_UNDO history[MAX_GAME_MOVES]; //history of game positions/moves (indexed by hisPly, used to undo moves and also check for repitition)

} S_BOARD;

// ***************** MACROS *****************

#define FR2SQ(f,r) ((21 + (f)) + ((r) * 10))    //for file and rank, return 120 index
#define SQ64(sq120) (sq120ToSq64[(sq120)])      //quick conversion to 64index
#define SQ120(sq64) (sq64ToSq120[(sq64)])       //quick conversion to 120index
#define POP(b) popBit(b)                        //make popbit a little easier
#define CNT(b) countBits(b)                     //easier countbits
#define CLRBIT(bb, sq) ((bb) &= clearMask[(sq)])//clear given bit in bitboard
#define SETBIT(bb, sq) ((bb) |= setMask[(sq)])  //set given bit in bitboard

#define ISN(p) (pieceKnight[(p)])               //check for piece types
#define ISB(p) (pieceBishop[(p)])
#define ISR(p) (pieceRook[(p)])
#define ISQ(p) (pieceQueen[(p)])
#define ISK(p) (pieceKing[(p)])


// ***************** GLOBALS *****************

extern int sq120ToSq64[BRD_SQ_NUM];     //convert padded board index to bitboard index
extern int sq64ToSq120[64];             //convert bitboard index to padded board index

extern U64 setMask[64];                 //for setting bit of bb
extern U64 clearMask[64];               //for clearing bit of bb

extern U64 pieceKeys[13][120];                 //hashing info
extern U64 sideKey;
extern U64 castleKeys[16];

extern char *pcChar[];                   //for printing
extern char sideChar[];
extern char rankChar[];
extern char fileChar[];

extern int pcBig[13];                   //easy lookup of piece attributes
extern int pcMaj[13];
extern int pcMin[13];
extern int pcVal[13];
extern int pcCol[13];

extern int filesBrd[BRD_SQ_NUM];        //get the file of given square
extern int ranksBrd[BRD_SQ_NUM];        //get the rank of given square

extern int pieceKnight[13];             //check for various piece types (more redundant bad coding on his part)
extern int pieceKing[13];
extern int pieceRook[13];
extern int pieceBishop[13];
extern int pieceQueen[13];

// ***************** FUNCTIONS *****************
//init.c
extern void allInit();

//bitboards.c
extern void printBitboard(U64 bb);
extern int popBit(U64 *bb);
extern int countBits(U64 b);

//hashkeys.c
extern U64 generatePosKey(const S_BOARD *pos);

//board.c
extern int parseFen(char *fen, S_BOARD *pos);
extern void resetBoard(S_BOARD *pos);
extern void printBoard(const S_BOARD *pos);
extern void updatePcLists(S_BOARD *pos);
extern int checkBoard(const S_BOARD *pos);

//attack.c
extern int sqAttacked(const int sq, const int side, const S_BOARD *pos);
extern void showSqAtkBySide(const int side, const S_BOARD *pos);

#endif
