import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

YELLOW = (200, 200, 200)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
cellSize = 50

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption("PAWN CHESS!!")
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

class Pawn:
    def __init__(self, color, position):
        self.color = color
        self.position = position # maintains position in (y,x)
        if (self.color == 'white'):
            self.image = pygame.image.load(r"C:\Users\hp\Downloads\whitepawn-removebg-preview.png")
        else:
            self.image = pygame.image.load(r"C:\Users\hp\Downloads\blackpawn-removebg-preview.png")
        self.image = pygame.transform.scale(self.image, (cellSize, cellSize))

    def draw(self, surface):
        surface.blit(self.image, (self.position[0] * cellSize, self.position[1] * cellSize))
    
    def showPossiblemoves(self,board): # return possible moves in (x,y) form x -> x coordinate , y -> y coordinate.
        possiblemoves=[] ## for each pawn I will calculate all possible moves and store in a list then highlight all these moves
        if self.color == 'white': direction = -1; oppCol = 'black'
        else: direction = 1; oppCol = 'white'

        x,y = self.position

        if (y+direction)<=7 and (y+direction)>=0:
            if board.grid[y+direction][x] is None:
                possiblemoves.append((x,y+direction))
        
        if (y==0 and self.color == 'black') or (y==7 and self.color=='white'):
            possiblemoves.append((x,y+2*direction))
        
        if (x+1)<=7 and (x+1)>=0 and (y+direction)<=7 and (y+direction)>=0:
            if board.grid[y+direction][x+1] is not None and board.grid[y+direction][x+1].color == oppCol:
                possiblemoves.append((x+1,y+direction))
        if (x-1)<=7 and (x-1)>=0 and (y+direction)<=7 and (y+direction)>=0:
            if board.grid[y+direction][x-1] is not None and board.grid[y+direction][x-1].color == oppCol:
                possiblemoves.append((x-1,y+direction))
      
        return possiblemoves


class Board:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = [[None for _ in range(8)] for _ in range(8)]  
        for i in range(len(self.grid[0])):
            self.grid[0][i]=Pawn('black', (i, 0))
        for i in range(len(self.grid[7])):
            self.grid[7][i]=Pawn('white', (i, 7))
        #self.grid[1][7] = Pawn('white',(7,1))
        self.selected_piece = None  
    
    def draw_board(self,possiblemoves):
        board = pygame.Surface((self.cell_size * 8, self.cell_size * 8),pygame.SRCALPHA)
        board_rect = board.get_rect(topleft=(200,100))
        board.fill((235, 235, 225))
        for x in range(0, 8, 1):
            for y in range(0, 8, 1):
                r = (x+y)%2
                if r == 0:
                    pygame.draw.rect(board, (100, 90, 150), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                if self.grid[y][x] is not None:
                    self.grid[y][x].draw(board) 

        for x,y in possiblemoves:
                cell_center = ((x * self.cell_size) + (self.cell_size // 2), (y * self.cell_size) + (self.cell_size // 2))
                pygame.draw.circle(board, (0, 205, 0, 125), cell_center, self.cell_size //4, 3) 
            #pygame.draw.rect(board,(0, 205, 0, 120),(x*cellSize,y*cellSize,cellSize,cellSize))
            
        screen.blit(board, board_rect)
    
    def checkwin(self):
        board = self.grid
        for i in range(board[0]):
            if board[0][i] is not None:
                if board[0][i].color == 'white':
                    ##white wins
        
        for i in range(board[7]):
            if board[7][i] is not None:


running = True

board = Board(cellSize)
turn = 'white'
possiblemoves=[]

while(running):
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    
    pressed_keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    x,y = mouse_pos
    grid_x,grid_y = (x-200)//cellSize,(y-100)//cellSize
    if  not (grid_x>7 or grid_x<0 or grid_y>7 or grid_y<0):
        
        if (board.grid[grid_y][grid_x] is not None and board.grid[grid_y][grid_x].color==turn and (pygame.mouse.get_pressed()[2] or pygame.mouse.get_pressed()[1] or pygame.mouse.get_pressed()[0])):
            #print(board.grid[y][x].color)
            possiblemoves = board.grid[grid_y][grid_x].showPossiblemoves(board)
            board.selected_piece = board.grid[grid_y][grid_x]
            print("now we are updating the possiblemoves")
        elif board.selected_piece is not None and (grid_x,grid_y) in possiblemoves and (pygame.mouse.get_pressed()[2] or pygame.mouse.get_pressed()[1] or pygame.mouse.get_pressed()[0]):
               ## selected pawn move to (grid_x,grid_y)
            x,y = board.selected_piece.position
            board.grid[y][x] = None
            board.selected_piece.position = (grid_x,grid_y)
            board.grid[grid_y][grid_x] = board.selected_piece 
            if turn == 'white':
                turn = 'black'
            elif turn == 'black':
                turn = 'white'           
            board.selected_piece = None
            possiblemoves = []
            
        elif board.grid[grid_y][grid_x] is None and (pygame.mouse.get_pressed()[2] or pygame.mouse.get_pressed()[1] or pygame.mouse.get_pressed()[0]):
            possiblemoves=[]

    screen.fill(YELLOW)
    board.draw_board(possiblemoves)
    
    pygame.display.update()



