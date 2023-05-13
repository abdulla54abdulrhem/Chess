#get input and display the current state

import pygame as p
from Chess import ChessEngine

HEIGHT = WIDTH = 512
DIMENSION = 8
SQ_SZ = HEIGHT // DIMENSION
MAX_FPS = 30
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
    print(gs.board)
    #then we load our images before the work
    loadImages()
    ttrue = True
    while ttrue:
        for e in p.event.get():
            if e.type == p.QUIT:
                ttrue = False
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