# Game Logic for loRes Chess
import enum

# enum for piece types
class PieceType(enum.Enum):
    EMPTY = enum.auto()
    PAWN = enum.auto()
    BISHOP = enum.auto()
    KNIGHT = enum.auto()
    ROOK = enum.auto()
    QUEEN = enum.auto()
    KING = enum.auto()

# enum for piece color
class Color(enum.Enum):
    WHITE = 0
    BLACK = 1

#enum for easy translation of space notation
class Space(enum.Enum):
    a1 = enum.auto()
    a2 = enum.auto()
    a3 = enum.auto()
    a4 = enum.auto()
    a5 = enum.auto()
    a6 = enum.auto()
    a7 = enum.auto()
    a8 = enum.auto()
    b1 = enum.auto()
    b2 = enum.auto()
    b3 = enum.auto()
    b4 = enum.auto()
    b5 = enum.auto()
    b6 = enum.auto()
    b7 = enum.auto()
    b8 = enum.auto()
    c1 = enum.auto()
    c2 = enum.auto()
    c3 = enum.auto()
    c4 = enum.auto()
    c5 = enum.auto()
    c6 = enum.auto()
    c7 = enum.auto()
    c8 = enum.auto()
    d1 = enum.auto()
    d2 = enum.auto()
    d3 = enum.auto()
    d4 = enum.auto()
    d5 = enum.auto()
    d6 = enum.auto()
    d7 = enum.auto()
    d8 = enum.auto()
    e1 = enum.auto()
    e2 = enum.auto()
    e3 = enum.auto()
    e4 = enum.auto()
    e5 = enum.auto()
    e6 = enum.auto()
    e7 = enum.auto()
    e8 = enum.auto()
    f1 = enum.auto()
    f2 = enum.auto()
    f3 = enum.auto()
    f4 = enum.auto()
    f5 = enum.auto()
    f6 = enum.auto()
    f7 = enum.auto()
    f8 = enum.auto()
    g1 = enum.auto()
    g2 = enum.auto()
    g3 = enum.auto()
    g4 = enum.auto()
    g5 = enum.auto()
    g6 = enum.auto()
    g7 = enum.auto()
    g8 = enum.auto()
    h1 = enum.auto()
    h2 = enum.auto()
    h3 = enum.auto()
    h4 = enum.auto()
    h5 = enum.auto()
    h6 = enum.auto()
    h7 = enum.auto()
    h8 = enum.auto()

#convert letter coord to number coord
l_to_n = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
}

#game: holds the board and info about game such as turn, move number, etc
class Game():
    def __init__(self):
        self.board = Board()
        self.board.setupBoard()
        self.turn = Color.WHITE         #TODO: for later remember can flip turn with not(self.turn)
        self.moveNumber = 1


# the board for the given game, holds the pieces
class Board():
    def __init__(self):
        #board state is a list of pieces (8 * row + column to access)
        self.state = []


    # always starts the same, so hardcode positions
    def setupBoard(self):
        state = []
        #make everything empty, then go through and add pieces
        for i in range(8):
            if (i % 2 == 0):
                for j in range(4):
                    temp = Piece(PieceType.EMPTY, Color.WHITE)
                    state.append(temp)
                    temp = Piece(PieceType.EMPTY, Color.BLACK)
                    state.append(temp)
            else:
                for j in range(4):
                    temp = Piece(PieceType.EMPTY, Color.BLACK)
                    state.append(temp)
                    temp = Piece(PieceType.EMPTY, Color.WHITE)
                    state.append(temp)
        #add pawns
        for i in range(8):
            state[8 * 1 + i] = Piece(PieceType.PAWN, Color.WHITE)
            state[8 * 6 + i] = Piece(PieceType.PAWN, Color.BLACK)

        #add minor pieces
        state[8 * 0 + 1] = Piece(PieceType.KNIGHT, Color.WHITE)
        state[8 * 0 + 6] = Piece(PieceType.KNIGHT, Color.WHITE)
        state[8 * 7 + 1] = Piece(PieceType.KNIGHT, Color.BLACK)
        state[8 * 7 + 6] = Piece(PieceType.KNIGHT, Color.BLACK)
        state[8 * 0 + 2] = Piece(PieceType.BISHOP, Color.WHITE)
        state[8 * 0 + 5] = Piece(PieceType.BISHOP, Color.WHITE)
        state[8 * 7 + 2] = Piece(PieceType.BISHOP, Color.BLACK)
        state[8 * 7 + 5] = Piece(PieceType.BISHOP, Color.BLACK)

        #add major pieces
        state[8 * 0 + 0] = Piece(PieceType.ROOK, Color.WHITE)
        state[8 * 0 + 7] = Piece(PieceType.ROOK, Color.WHITE)
        state[8 * 7 + 0] = Piece(PieceType.ROOK, Color.BLACK)
        state[8 * 7 + 7] = Piece(PieceType.ROOK, Color.BLACK)
        state[8 * 0 + 3] = Piece(PieceType.QUEEN, Color.WHITE)
        state[8 * 7 + 3] = Piece(PieceType.QUEEN, Color.BLACK)
        state[8 * 0 + 4] = Piece(PieceType.KING, Color.WHITE)
        state[8 * 7 + 4] = Piece(PieceType.KING, Color.BLACK)

        self.state = state

    #get piece given coords (so don't need to do that ugly math)
    def getPieceXY(self, rank, file):
        return self.state[8 * rank + file]


# pieces: type, color
class Piece():
    def __init__(self, type, color):
        #both type and color are enums
        self.type = type
        self.color = color

#convert classic chess coordinate to index in array
def coordToIndex(c):
    x = l_to_n[c[0]]
    y = int(c[1]) - 1
    return 8 * x + y

#testing
# g = Game()
# for p in g.board.state:
#     print(p.type, p.color)
