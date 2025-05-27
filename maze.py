import pygame
import random
import time

ROWS, COLS = 45,45
CELL_SIZE = 10
WIDTH,HEIGHT = ROWS * CELL_SIZE,COLS * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0,255,0)
RED = (255,0,0)
PINK = (252,15,192)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# random.seed(4)

class Maze:
    def __init__(self, rows:int,cols:int,cell_size:int) -> None:
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.start_time = 0
        self.end_time = 0
        self.finished = False

    def draw_maze(self,playerX:int,playerY:int,dont:bool=False) -> None:
        if dont != True:
            self.matrix[playerX][playerY] = 3
        screen.fill(BLACK)
        for row in range(self.rows):
            for col in range(self.cols):
                match self.matrix[row][col]:
                    case 0:
                        color = WHITE
                    case 1:
                        color = BLACK
                    case 2:
                        color = GREEN
                    case 3:
                        color = BLUE
                    case 4:
                        color = RED
                    case 5:
                        color = PINK
                pygame.draw.rect(screen, color, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.update()
        if dont != True:
             self.matrix[playerX][playerY] = 4


    #1.Losowy node 2.Zrób ścieżke 3.Sąsiedzi co 2 jeżeli są ściany to robie przejście pomiedzy i tak dla każdego neighbora 
    #4. jak nie ma już ścian obok neighbora to cofasz do ostatniego miejsca z neighbor 5. Jak nie ma już do czego cofać to koniec
    #W mojej implementacji zaczyna od losowego miejsca losuje kolejność sąsiadów i dla każdego rusza się do neighbora ustawia na 0
    #Od tamtego miejsca znowu backtracking rekursywnie i jak się skończy to wraca
    def generate_maze(self,multiple_paths:bool = False):
        self.matrix = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        start_row, start_col = (random.randrange(1, self.rows-1, 2), random.randrange(1, self.cols-1, 2))
        self.startX, self.startY = random.randrange(1, self.rows, 2), self.cols-1
        self.exitX, self.exitY = random.randrange(1, self.rows, 2), 0
        def backtracking(self,row:int,col:int):
            self.matrix[row][col] = 0
            self.draw_maze(self.startX,self.startY,False)

            random.shuffle(self.directions)
            for dx, dy in self.directions:
                new_row, new_col = row + dx * 2, col + dy * 2
                if 1 <= new_row < self.rows-1 and 1 <= new_col < self.cols-1 and self.matrix[new_row][new_col] == 1:
                    self.matrix[row + dx][col + dy] = 0
                    backtracking(self,new_row,new_col)
        
        backtracking(self,start_row,start_col)
        #losuje miejsce musi oś x lub oś y być pusta a reszta pełna by móc usunać ściane
        if multiple_paths == True:
            removed_walls = 0
            while removed_walls < 30:
                random_x = random.randrange(2,self.rows-1,2)
                random_y = random.randrange(2,self.cols-1,2)
                neighbor_walls = [(random_x-1,random_y),(random_x+1,random_y),(random_x,random_y-1),(random_x,random_y+1)]
                walls_x = 0
                walls_y = 0
                if self.matrix[random_x][random_y] == 1:
                    if self.matrix[neighbor_walls[0][0]][neighbor_walls[0][1]] == 1:
                        walls_x += 1
                    if self.matrix[neighbor_walls[1][0]][neighbor_walls[1][1]] == 1:
                        walls_x += 1
                    if self.matrix[neighbor_walls[2][0]][neighbor_walls[2][1]] == 1:
                        walls_y += 1
                    if self.matrix[neighbor_walls[3][0]][neighbor_walls[3][1]] == 1:
                        walls_y += 1
                    if walls_x == 2 and walls_y == 2:
                        continue
                    elif walls_x == 1 or walls_y == 1:
                        continue
                    else:
                        self.matrix[random_x][random_y] = 0
                        removed_walls += 1
                        self.draw_maze(self.startX,self.startY)
          
        self.matrix[self.startX][self.startY] = 3
        self.matrix[self.exitX][self.exitY] = 2
        self.draw_maze(self.startX,self.startY)
        self.start_time = time.time()

    def check_win(self,playerX:int,playerY:int):
        if playerX == self.exitX and playerY == self.exitY or self.finished == True:
            self.end_time = time.time()
            self.end_message()
            return True

    def end_message(self):
        solve_time = self.end_time - self.start_time
        print(f"Time:{round(solve_time,3)}")
