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
    def getPiece(self, rank, file):
        return self.state[8 * rank + file]

    #change what piece is at given spot on board
    def putPiece(self, rank, file, piece):
        self.state[8 * rank + file] = piece

# pieces: type, color
class Piece():
    def __init__(self, type, color):
        #both type and color are enums
        self.type = type
        self.color = color


#testing
# g = Game()
# for p in g.board.state:
#     print(p.type, p.color)
