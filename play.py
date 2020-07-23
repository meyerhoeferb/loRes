#file that is run to play the game, controls CLI

import logic
Color = logic.Color
PieceType = logic.PieceType
Space = logic.Space

#welcome and prompt for option
def cli():
    print("Welcome to loRes Chess\n")
    while(True):
        printMenu()
        option = input(">   ")
        if(option == 'play'):
            play()
        elif(option == 'quit'):
            print("Thanks for playing")
            break
        else:
            print(option + " is not a recognized option\n")

#initiate game logic
def play():
    game = logic.Game()
    showBoard(game)


#found special characters online for ascii board visualization
chrs = {
    (Color.WHITE, PieceType.EMPTY): "\u25FB",
    (Color.WHITE, PieceType.PAWN): "\u265F",
    (Color.WHITE, PieceType.ROOK): "\u265C",
    (Color.WHITE, PieceType.KNIGHT): "\u265E",
    (Color.WHITE, PieceType.BISHOP): "\u265D",
    (Color.WHITE, PieceType.KING): "\u265A",
    (Color.WHITE, PieceType.QUEEN): "\u265B",
    (Color.BLACK, PieceType.EMPTY): "\u25FC",
    (Color.BLACK, PieceType.PAWN): "\u2659",
    (Color.BLACK, PieceType.ROOK): "\u2656",
    (Color.BLACK, PieceType.KNIGHT): "\u2658",
    (Color.BLACK, PieceType.BISHOP): "\u2657",
    (Color.BLACK, PieceType.KING): "\u2654",
    (Color.BLACK, PieceType.QUEEN): "\u2655",
}

#print board in command line
def showBoard(game):
    #handles flipping of board based on whose turn it is
    if(game.turn == Color.WHITE):
        row_order = range(7,-1,-1)
        col_order = range(8)
    else:
        row_order = range(8)
        col_order = range(7,-1,-1)
    for i in row_order:
        for j in col_order:
            p = game.board.getPieceXY(i,j)
            print(chrs[(p.color,p.type)], end=' ')
        print()


#print menu options
def printMenu():
    print('play')
    print('quit')


if __name__ == '__main__':
    cli()
