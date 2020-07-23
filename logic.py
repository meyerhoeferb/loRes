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
        self.turn = Color.WHITE         #TODO: for later remember can flip turn with not(self.turn)
        self.castlePriv = ''            #castling availability, keep fen notation
        self.ply = 1                    #count half moves for draw condition
        self.move = 1                   #count full moves, inc after black move
        self.enpas = -1                #index of en passant target, -1 if none

    #parse given fen file, used to start game but also to load positions
    def parseFen(self, fen_file):
        with open(fen_file, 'r') as file:
            fen = file.read().replace('\n','')

        info = fen.split(' ')
        board = info[0]             #board position
        toMove = info[1]            #color to move
        self.castlePriv = info[2]   #castle privileges
        enpas = info[3]             #enpas target
        self.ply = info[4]          #half move clock (for draws)
        self.move = info[5]         #full move count

        if(toMove == 'w'):
            self.turn = Color.WHITE
        else:
            self.turn = Color.BLACK

        if(enpas == '-'):
            self.enpas = -1
        else:
            self.enpas = coordToIndex(enpas)

        rows = board.split('/')
        x = 7
        for r in rows:
            y = 0
            for p in r:
                if(p == 'p'):
                    self.board.putPieceXY(x,y,PieceType.PAWN, Color.BLACK)
                elif(p == 'P'):
                    self.board.putPieceXY(x,y,PieceType.PAWN, Color.WHITE)
                elif(p == 'n'):
                    self.board.putPieceXY(x,y,PieceType.KNIGHT, Color.BLACK)
                elif(p == 'N'):
                    self.board.putPieceXY(x,y,PieceType.KNIGHT, Color.WHITE)
                elif(p == 'b'):
                    self.board.putPieceXY(x,y,PieceType.BISHOP, Color.BLACK)
                elif(p == 'B'):
                    self.board.putPieceXY(x,y,PieceType.BISHOP, Color.WHITE)
                elif(p == 'r'):
                    self.board.putPieceXY(x,y,PieceType.ROOK, Color.BLACK)
                elif(p == 'R'):
                    self.board.putPieceXY(x,y,PieceType.ROOK, Color.WHITE)
                elif(p == 'q'):
                    self.board.putPieceXY(x,y,PieceType.QUEEN, Color.BLACK)
                elif(p == 'Q'):
                    self.board.putPieceXY(x,y,PieceType.QUEEN, Color.WHITE)
                elif(p == 'k'):
                    self.board.putPieceXY(x,y,PieceType.KING, Color.BLACK)
                elif(p == 'K'):
                    self.board.putPieceXY(x,y,PieceType.KING, Color.WHITE)
                else:
                    for i in range(int(p)):
                        y += 1
                        continue
                y+=1
            x -= 1


# the board for the given game, holds the pieces
class Board():
    def __init__(self):
        #board state is a list of pieces, initialize all empty squares
        self.state = []
        for i in range(8):
            if (i % 2 == 0):
                for j in range(4):
                    temp = Piece(PieceType.EMPTY, Color.WHITE)
                    self.state.append(temp)
                    temp = Piece(PieceType.EMPTY, Color.BLACK)
                    self.state.append(temp)
            else:
                for j in range(4):
                    temp = Piece(PieceType.EMPTY, Color.BLACK)
                    self.state.append(temp)
                    temp = Piece(PieceType.EMPTY, Color.WHITE)
                    self.state.append(temp)

    #get piece given coords (so don't need to do that ugly math)
    def getPieceXY(self, x, y):
        return self.state[8 * x + y]

    #place a piece on the given square
    def putPieceXY(self, x, y, type, color):
        self.state[8 * x + y] = Piece(type, color)


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
