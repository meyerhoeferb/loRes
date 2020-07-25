'''
the engine:

logic for move generation and search
main will have options for starting in uci or xboard mode
'''
import enum

# enum for piece types
class PieceType(enum.Enum):
    EMPTY = enum.auto()
    PAWN = enum.auto()
    KNIGHT = enum.auto()
    BISHOP = enum.auto()
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
    'origin': 0b0000000000000000000001111111,   #where piece comes from
    'dest': 0b0000000000000011111110000000,     #where piece going to
    'captured': 0b0000000000111100000000000000, #what does it capture
    'ep': 0b0000000001000000000000000000,  #en passant capture
    'ps': 0b0000000010000000000000000000,  #pawn start
    'promote': 0b0000111100000000000000000000,  #what does it promote to
    'castle': 0b0001000000000000000000000000,   #is this move a castle
    'score': 0b1110000000000000000000000000,    #move score for move ordering in search
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
    'score': 25,
}
#key for ranking of various types of moves
move_scores = {
    'none': 0,
    'prom': 1,
    'cap': 2,
}


# the board for the given game, holds all info about game
class Board():
    def __init__(self):
        #array of white and blacks current material, index using enum values
        #first index is empty squares so number doesn't matter
        self.white_mat = [0, 8, 2, 2, 2, 1, 1]
        self.black_mat = [0, 8, 2, 2, 2, 1, 1]
        self.moveGen = MoveGenerator()
        self.turn = Color.WHITE         #TODO: for later remember can flip turn with not(self.turn)
        self.castlePriv = ''            #castling availability, keep fen notation
        self.ply = 1                    #count half moves for draw condition
        self.move = 1                   #count full moves, inc after black move
        self.enpas = -1                 #index of en passant target, -1 if none
        #board state is a list of pieces, initialize all empty squares
        self.state = []
        for i in range(8):
            for j in range(8):
                self.state.append(Piece(PieceType.EMPTY, Color.WHITE))

    #get piece given coords
    def getPieceXY(self, x, y):
        return self.state[8 * x + y]

    #place a piece on the given square
    def putPieceXY(self, x, y, type, color):
        self.state[8 * x + y] = Piece(type, color)

    #parse given fen string, used to setup board states given by cli
    def parseFen(self, fen):

        info = fen.split(' ')
        board = info[0]                     #board position
        toMove = info[1]                    #color to move
        self.castlePriv = info[2]           #castle privileges
        enpas = info[3]                     #enpas target (given as chess, later made and stored as index)
        self.ply = info[4]                  #half move clock (for draws)
        self.move = info[5]                 #full move count

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
                    self.putPieceXY(x,y,PieceType.PAWN, Color.BLACK)
                elif(p == 'P'):
                    self.putPieceXY(x,y,PieceType.PAWN, Color.WHITE)
                elif(p == 'n'):
                    self.putPieceXY(x,y,PieceType.KNIGHT, Color.BLACK)
                elif(p == 'N'):
                    self.putPieceXY(x,y,PieceType.KNIGHT, Color.WHITE)
                elif(p == 'b'):
                    self.putPieceXY(x,y,PieceType.BISHOP, Color.BLACK)
                elif(p == 'B'):
                    self.putPieceXY(x,y,PieceType.BISHOP, Color.WHITE)
                elif(p == 'r'):
                    self.putPieceXY(x,y,PieceType.ROOK, Color.BLACK)
                elif(p == 'R'):
                    self.putPieceXY(x,y,PieceType.ROOK, Color.WHITE)
                elif(p == 'q'):
                    self.putPieceXY(x,y,PieceType.QUEEN, Color.BLACK)
                elif(p == 'Q'):
                    self.putPieceXY(x,y,PieceType.QUEEN, Color.WHITE)
                elif(p == 'k'):
                    self.putPieceXY(x,y,PieceType.KING, Color.BLACK)
                elif(p == 'K'):
                    self.putPieceXY(x,y,PieceType.KING, Color.WHITE)
                else:
                    for i in range(int(p)):
                        self.putPieceXY(x,y,PieceType.EMPTY, Color.WHITE) #just make all empty black (for some reason flips)
                        y += 1
                        continue
                y+=1
            x -= 1

    #update the move generator, just here so CLI doesn't need to access generator
    def findMoves(self):
        self.moveGen.updateMoves(self)


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
        self.foundMoves = []

    #find moves by going through board state and following rules for found pieces
    #TODO: somewhere in the beginning of this, if a color is in check their moves
    #are limited only things that stop check and that requires its own logic (maybe pass if we're in check??)
    def updateMoves(self, board):
        #iterate through all spots and collect valid moves for appropriate pieces
        color = board.turn
        self.foundMoves = []
        for i, space in enumerate(board.state):
            if(space.type == PieceType.EMPTY or space.color != color):
                continue

            #calculate x,y of piece
            x = i // 8
            y = i % 8

            #pawn rules FIXME: rn only promotes to queen, should eventually add 4 moves in that scenario, one for each promote
            if(space.type == PieceType.PAWN):
                #set up vertical movement for different colors
                if(color == Color.WHITE):
                    yDir = 1
                    promRow = 7
                else:
                    yDir = -1
                    promRow = 2

                #check space in front
                checkX = x + 0
                checkY = y + yDir
                #validate space
                if(checkX < 8 and checkX >= 0 and checkY < 8 and checkY >= 0):
                    checkPiece = board.getPieceXY(checkX, checkY)
                    if(checkPiece.type == PieceType.EMPTY):
                        newOri = coordToIndex(x,y)
                        newDest = coordToIndex(checkX, checkY)
                        newCap = 0
                        newEp = 0
                        newPs = 0
                        newPromote = 0  #make zero, before adding move will check for promotion possibility
                        newCastle = 0
                        newScore = 0
                        if(x == promRow):
                            newScore = move_scores['prom']
                            self.foundMoves.append(createMove(newOri, newDest, newCap, newEp, newPs, PieceType.KNIGHT.value, newCastle, newScore))
                            self.foundMoves.append(createMove(newOri, newDest, newCap, newEp, newPs, PieceType.BISHOP.value, newCastle, newScore))
                            self.foundMoves.append(createMove(newOri, newDest, newCap, newEp, newPs, PieceType.ROOK.value, newCastle, newScore))
                            self.foundMoves.append(createMove(newOri, newDest, newCap, newEp, newPs, PieceType.QUEEN.value, newCastle, newScore))
                        else:
                            self.foundMoves.append(createMove(newOri, newDest, newCap, newEp, newPs, newPromote, newCastle, newScore))


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
                            newScore = 0
                            self.foundMoves.append(createMove(newOri, newDest, newCap, newEp, newPs, newPromote, newCastle, newScore))
                        #if not empty but of opposite color and not a king then add
                        elif(checkPiece.color != color and checkPiece.type != PieceType.KING):
                            newOri = coordToIndex(x,y)
                            newDest = coordToIndex(checkX, checkY)
                            newCap = checkPiece.type.value      #get number corresponding to piece enum
                            newEp = 0       #nothing from here on is possible for knights
                            newPs = 0
                            newPromote = 0
                            newCastle = 0
                            newScore = move_scores['cap']
                            self.foundMoves.append(createMove(newOri, newDest, newCap, newEp, newPs, newPromote, newCastle, newScore))

            #slider rules
            if(space.type == PieceType.BISHOP):
                delta = [(1,1), (1,-1), (-1,1), (-1,-1)]
            elif(space.type == PieceType.ROOK):
                delta = [(1,0), (-1,0), (0,1), (0,-1)]
            elif(space.type == PieceType.QUEEN):
                delta = [(1,1), (1,-1), (-1,1), (-1,-1), (1,0), (-1,0), (0,1), (0,-1)]

                for d in delta:
                    checkX = x + d[0]
                    checkY = y + d[1]
                    #follow this direction until leave board or hit something
                    while(True):
                        if(not(checkX < 8 and checkX >= 0 and checkY < 8 and checkY >= 0)):
                            break
                        checkPiece = board.getPieceXY(checkX, checkY)
                        if(checkPiece.type == PieceType.EMPTY):
                            newOri = coordToIndex(x,y)
                            newDest = coordToIndex(checkX, checkY)
                            newCap = 0
                            newEp = 0       #nothing from here on is possible for knights
                            newPs = 0
                            newPromote = 0
                            newCastle = 0
                            newScore = 0
                            self.foundMoves.append(createMove(newOri, newDest, newCap, newEp, newPs, newPromote, newCastle, newScore))
                        elif(checkPiece.color != color and checkPiece.type != PieceType.KING):
                            newOri = coordToIndex(x,y)
                            newDest = coordToIndex(checkX, checkY)
                            newCap = checkPiece.type.value      #get number corresponding to piece enum
                            newEp = 0
                            newPs = 0
                            newPromote = 0
                            newCastle = 0
                            newScore = move_scores['cap']
                            self.foundMoves.append(createMove(newOri, newDest, newCap, newEp, newPs, newPromote, newCastle, newScore))
                            break
                        elif(checkPiece.color == color or checkPiece.type == PieceType.KING):
                            break

                        #go to next possible position in this direction if didn't break
                        checkX = x + d[0]
                        checkY = y + d[1]


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
def createMove(origin, dest, captured, ep, ps, promote, castle, score):
    bDest = dest << shift_dict['dest']
    bCap = captured << shift_dict['captured']
    bEp = ep << shift_dict['ep']
    bPs = ps << shift_dict['ps']
    bProm = promote << shift_dict['promote']
    bCastle = castle << shift_dict['castle']
    bScore = score << shift_dict['score']

    return origin + bDest + bCap + bEp + bPs + bProm + bCastle + bScore

#testing
# g = Game()
# for p in g.board.state:
#     print(p.type, p.color)
