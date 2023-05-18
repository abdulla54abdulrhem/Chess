#get input and display the current state

import pygame as p
from Chess import ChessEngine

HEIGHT = WIDTH = 512
DIMENSION = 8
SQ_SZ = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

#in the start of the program we will load the images needed
def loadImages():
    pcs = ['wp','wN','wB','wQ','wK','wR','bp','bN','bB','bQ','bK','bR']
    for pc in pcs:
        IMAGES[pc] = p.transform.scale(p.image.load("images/"+pc+".png"),(SQ_SZ,SQ_SZ))

#the main driver, this will handle the input and update the graphics depending on the state

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()

    moveMade = False #flag for when a move is made
    print(gs.board)
    #then we load our images before the work
    loadImages()
    ttrue = True
    sqSelected = ()
    playerClicks = []
    validMoves = gs.getValidMoves()

    while ttrue:

        for e in p.event.get():
            if e.type == p.QUIT:
                ttrue = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN :
                location = p.mouse.get_pos()
                col = location[0] // SQ_SZ
                row = location[1] // SQ_SZ
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
                    print('start new clicks now')

            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawBoard(screen):
    colors = [p.Color("light gray"), p.Color('gray')]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i+j)%2)]
            p.draw.rect(screen,color,p.Rect(j*SQ_SZ,i*SQ_SZ,SQ_SZ,SQ_SZ))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            pc = board[r][c]
            if pc != "--":
                screen.blit(IMAGES[pc], p.Rect(c*SQ_SZ, r*SQ_SZ, SQ_SZ, SQ_SZ))

def drawGameState(screen,gameState):
    drawBoard(screen)
    drawPieces(screen,gameState.board)

if __name__ == "__main__":
    main()