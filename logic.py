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

#convert number coord to letter coord
n_to_l = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

#move information will be stored as binary numbers
#use the mask to isolate info from the number
move_mask_dict = {
    'origin': 0b0000000000000000000001111111,
    'dest': 0b0000000000000011111110000000,
    'captured': 0b0000000000111100000000000000,
    'ep': 0b0000000001000000000000000000,  #en passant capture
    'ps': 0b0000000010000000000000000000,  #pawn start
    'promote': 0b0000111100000000000000000000,
    'castle': 0b0001000000000000000000000000,
} #to print x use format(x,'028b')   (prints 28 bits with left padding)
#use the shift to create moves and access info
shift_dict = {
    'origin': 0,
    'dest': 7,
    'captured': 14,
    'ep': 18,
    'ps': 19,
    'promote': 23,
    'castle': 24,
}

#game: holds the board and info about game such as turn, move number, etc
class Game():
    def __init__(self):
        self.board = Board()
        self.moveGen = MoveGenerator()
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
            self.enpas = chessToIndex(enpas)

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

    #update the move generator, just here so CLI doesn't need to access generator
    def findMoves(self):
        self.moveGen.updateMoves(self.board, self.turn)


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

    #get piece given coords
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


#move generator
#moves are always a 4 char string of format origindest for instance 'e2e4'
class MoveGenerator():
    def __init__(self):
        self.whiteMoves = []
        self.blackMoves = []

    #find moves by going through board state and following rules for found pieces
    #TODO: somewhere in the beginning of this, if a color is in check their moves
    #are limited only things that stop check and that requires its own logic (maybe pass if we're in check??)
    def updateMoves(self, board, color):
        #iterate through all spots and collect valid moves for appropriate pieces
        foundMoves = []
        for i, space in enumerate(board.state):
            if(space.type == PieceType.EMPTY or space.color != color):
                continue

            #calculate x,y of piece
            x = i // 8
            y = i % 8

            #knight rules
            if(space.type == PieceType.KNIGHT):
                delta = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)] #possible changes in coord

                for d in delta:
                    checkX = x + d[0]
                    checkY = y + d[1]
                    #validate space
                    if(checkX < 8 and checkX >= 0 and checkY < 8 and checkY >= 0):
                        checkPiece = board.getPieceXY(checkX, checkY)
                        #if empty then valid and add to appropriate list
                        if(checkPiece.type == PieceType.EMPTY):
                            newOri = coordToIndex(x,y)
                            newDest = coordToIndex(checkX, checkY)
                            newCap = 0
                            newEp = 0       #nothing from here on is possible for knights
                            newPs = 0
                            newPromote = 0
                            newCastle = 0
                            foundMoves.append(createMove(newOri, newDest, newCap, newEp, newPs, newPromote, newCastle))
                        #if not empty but of opposite color and not a king then add
                        elif(checkPiece.color != color and checkPiece.type != PieceType.KING):
                            newOri = coordToIndex(x,y)
                            newDest = coordToIndex(checkX, checkY)
                            newCap = checkPiece.type.value      #get number corresponding to piece enum
                            newEp = 0       #nothing from here on is possible for knights
                            newPs = 0
                            newPromote = 0
                            newCastle = 0
                            foundMoves.append(createMove(newOri, newDest, newCap, newEp, newPs, newPromote, newCastle))

        #udpate appropriate move list with found moves
        if(color == Color.WHITE):
            self.whiteMoves = foundMoves[:]
        else:
            self.blackMoves = foundMoves[:]


#convert classic chess coordinate to index in array
def chessToIndex(c):
    x = l_to_n[c[0]]
    y = int(c[1]) - 1
    return 8 * x + y

#convert x,y coords to index in array
def coordToIndex(x, y):
    return 8 * x + y

#convert coord to chess notation
def coordToChess(x,y):
    return n_to_l[x] + str(y + 1)

#create a move with the given info
def createMove(origin, dest, captured, ep, ps, promote, castle):
    bDest = dest << shift_dict['dest']
    bCap = captured << shift_dict['captured']
    bEp = ep << shift_dict['ep']
    bPs = ps << shift_dict['ps']
    bProm = promote << shift_dict['promote']
    bCastle =castle << shift_dict['castle']

    return origin + bDest + bCap + bEp + bPs + bProm + bCastle

#testing
# g = Game()
# for p in g.board.state:
#     print(p.type, p.color)
