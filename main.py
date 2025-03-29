import pygame
import random
import keyboard
from typing import Literal
import time

ROWS, COLS = 41,41
CELL_SIZE = 10
WIDTH,HEIGHT = ROWS * CELL_SIZE,COLS * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0,255,0)
RED = (255,0,0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Maze:
    def __init__(self, rows,cols,cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.current_direction: Literal["up", "down", "left", "right"] = "left"
        self.positions: Literal["up", "down", "left", "right","stay"] = "stay"
        self.start_time = 0
        self.end_time = 0
    def set_positions(self, pos):
        self.positions = pos
    
    def set_direction(self,dir):
        self.current_direction = dir

    def draw_maze(self,maze:list):
        maze[self.playerX][self.playerY] = 3
        screen.fill(BLACK)
        for row in range(self.rows):
            for col in range(self.cols):
                if maze[row][col] == 0:
                    color = WHITE
                if maze[row][col] == 1:
                    color = BLACK
                if maze[row][col] == 2:
                    color = GREEN
                if maze[row][col] == 3:
                    color = BLUE
                if maze[row][col] == 4:
                    color = RED
                pygame.draw.rect(screen, color, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.update()
        maze[self.playerX][self.playerY] = 4

    def generate_maze(self):
        self.maze = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        start_row, start_col = (random.randrange(1, self.rows-1, 2), random.randrange(1, self.cols-1, 2))
        self.playerX, self.playerY = random.randrange(1, self.rows, 2), self.cols-1
        self.exit_x, self.exit_y = random.randrange(1, self.rows, 2), 0
    
        def backtracking(self,row:int,col:int):
            self.maze[row][col] = 0
            self.draw_maze(self.maze)
            
            random.shuffle(self.directions)
            for dx, dy in self.directions:
                new_row, new_col = row + dx * 2, col + dy * 2
                if 1 <= new_row < self.rows-1 and 1 <= new_col < self.cols-1 and self.maze[new_row][new_col] == 1:
                    self.maze[row + dx][col + dy] = 0
                    backtracking(self,new_row,new_col)
        # i = 0
        # while i<20:
        #     i += 1
        #     random_x = random.randrange(0,self.rows,2)
        #     random_y = random.randrange(0,self.cols,2)
        #     self.maze[random_x][random_y] = 0
        backtracking(self,start_row,start_col)
        self.maze[self.playerX][self.playerY] = 3
        self.maze[self.exit_x][self.exit_y] = 2
        self.draw_maze(self.maze)
        self.start_time = time.time()
    def move_player(self):
        match self.positions:
            case "left":
                if self.playerY == 0:
                    self.playerY = 0
                elif self.maze[self.playerX][self.playerY-1] == 1:
                    pass
                else:
                    self.playerY -= 1
            case "right":
                if self.playerY == self.rows - 1:
                    self.playerY = self.rows - 1
                elif self.maze[self.playerX][self.playerY+1] == 1:
                    pass
                else:
                    self.playerY += 1

            case "up":
                if self.playerX == 0:
                    self.playerX= 0
                elif self.maze[self.playerX-1][self.playerY] == 1:
                    pass
                else:
                    self.playerX-= 1
                
            case "down":
                if self.playerX == self.rows - 1:
                    self.playerX = self.rows - 1
                elif self.maze[self.playerX+1][self.playerY] == 1:
                    pass
                else:
                    self.playerX += 1
            case "stay":
                self.playerY = self.playerY
                self.playerX = self.playerX
        self.draw_maze(self.maze)
    def check_win(self):
        if self.playerX == self.exit_x and self.playerY == self.exit_y:
            self.end_time = time.time()
            return True

    def end_message(self):
        solve_time = self.end_time - self.start_time
        print(f"Time:{round(solve_time,3)}")

    def right_hand_solver(self):
        next_move = ""
        current_rigth = ""
        current_forward = ""
        match self.current_direction:
            case "left":
                current_rigth = self.maze[self.playerX-1][self.playerY]
                current_forward = self.maze[self.playerX][self.playerY-1]
                if current_rigth != 1:
                    next_move = "up"
                    self.set_direction("up")
                elif current_forward != 1:
                    next_move = "left"
                else:
                    self.set_direction("down")
            case "down":
                current_rigth = self.maze[self.playerX][self.playerY-1]
                current_forward = self.maze[self.playerX+1][self.playerY]
                if current_rigth != 1:
                    next_move = "left"
                    self.set_direction("left")
                elif current_forward != 1:
                    next_move = "down"
                else:
                    self.set_direction("right")
            case "right":
                current_rigth = self.maze[self.playerX+1][self.playerY]
                current_forward = self.maze[self.playerX][self.playerY+1]
                if current_rigth != 1:
                    next_move = "down"
                    self.set_direction("down")
                elif current_forward != 1:
                    next_move = "right"
                else:
                    self.set_direction("up")
            case "up":
                current_rigth = self.maze[self.playerX][self.playerY+1]
                current_forward = self.maze[self.playerX-1][self.playerY]
                if current_rigth != 1:
                    next_move = "right"
                    self.set_direction("right")
                elif current_forward != 1:
                    next_move = "up"
                else:
                    self.set_direction("left")

        self.set_positions(next_move)
        self.move_player()
        self.draw_maze(self.maze)

    def dfs_solver(self):
        stack = []
        neighbors = []
        if 0 <= self.playerX < self.rows - 1 and 0 <= self.playerY < self.cols - 1:
            neighbors = [(self.playerX,self.playerY-1),(self.playerX-1,self.playerY),(self.playerX+1,self.playerY),(self.playerX,self.playerY+1)]
        else:
            if self.playerY-1 >= 0:
                neighbors.append((self.playerX,self.playerY-1))
            if self.playerX-1 >= 0:
                neighbors.append((self.playerX-1,self.playerY))
            if self.playerX+1 < self.rows - 1:
                neighbors.append((self.playerX+1,self.playerY))
            if self.playerY+1 < self.cols - 1:
                neighbors.append((self.playerX,self.playerY+1))
        while self.check_win() != True:
            options = []
            for neighbor in neighbors:
                if self.maze[neighbor[0]][neighbor[1]] == 0 or self.maze[neighbor[0]][neighbor[1]] == 2:
                    options.append(neighbor)
            if len(options) > 1:
                stack.append((self.playerX,self.playerY))
                self.playerX,self.playerY = options[0][0],options[0][1]
                
            if len(options) == 1:
                self.playerX,self.playerY = options[0][0],options[0][1]
            
            if len(options) == 0:
                self.playerX,self.playerY = stack[-1][0],stack[-1][1]
                stack.pop(-1)

            if 0 <= self.playerX < self.rows - 1 and 0 <= self.playerY < self.cols - 1:
                neighbors = [(self.playerX,self.playerY-1),(self.playerX-1,self.playerY),(self.playerX+1,self.playerY),(self.playerX,self.playerY+1)]
            else:
                neighbors = []
                if self.playerY-1 >= 0:
                    neighbors.append((self.playerX,self.playerY-1))
                if self.playerX-1 >= 0:
                    neighbors.append((self.playerX-1,self.playerY))
                if self.playerX+1 < self.rows - 1:
                    neighbors.append((self.playerX+1,self.playerY))
                if self.playerY+1 < self.cols - 1:
                    neighbors.append((self.playerX,self.playerY+1))
            self.draw_maze(self.maze)
    
    def bfs_solver(self):
        queue = []
        parents = {}
        neighbors = []
        if 0 <= self.playerX < self.rows - 1 and 0 <= self.playerY < self.cols - 1:
            neighbors = [(self.playerX,self.playerY-1),(self.playerX-1,self.playerY),(self.playerX+1,self.playerY),(self.playerX,self.playerY+1)]
        else:
            if self.playerY-1 >= 0:
                neighbors.append((self.playerX,self.playerY-1,(self.playerX,self.playerY)))
            if self.playerX-1 >= 0:
                neighbors.append((self.playerX-1,self.playerY,(self.playerX,self.playerY)))
            if self.playerX+1 < self.rows - 1:
                neighbors.append((self.playerX+1,self.playerY,(self.playerX,self.playerY)))
            if self.playerY+1 < self.cols - 1:
                neighbors.append((self.playerX,self.playerY+1,(self.playerX,self.playerY)))
        while self.check_win() != True:
            for neighbor in neighbors:
                if self.maze[neighbor[0]][neighbor[1]] == 0:
                    queue.append(neighbor)
                    parents[(neighbor[0],neighbor[1])] = neighbor[2]
                    self.maze[neighbor[0]][neighbor[1]] = 4
                if self.maze[neighbor[0]][neighbor[1]] == 2:
                    parents[(neighbor[0],neighbor[1])] = neighbor[2]
                    self.playerX,self.playerY = neighbor[0],neighbor[1]
            
            neighbors = []
            for element in queue:
                if element[1]-1 >= 0:
                    neighbors.append((element[0],element[1]-1,(element[0],element[1])))
                if element[0]-1 >= 0:
                    neighbors.append((element[0]-1,element[1],(element[0],element[1])))
                if element[0]+1 < self.rows - 1:
                    neighbors.append((element[0]+1,element[1],(element[0],element[1])))
                if element[1]+1 < self.cols - 1:
                    neighbors.append((element[0],element[1]+1,(element[0],element[1])))
            queue.pop(0)
            self.draw_maze(self.maze)
        
        shortest_path_created = False
        next_cell = parents[(self.playerX,self.playerY)]
        while not shortest_path_created:
            self.maze[next_cell[0]][next_cell[1]] = 2
            self.draw_maze(self.maze)
            try:
                next_cell = parents[(next_cell[0],next_cell[1])]
            except:
                break
        
    def dead_end_solver(self):
            _____ = {}
            _____ = [(self.playerX,self.playerY-1)]
            path_created = False
            while path_created != True:
                for cell in ____:
                    walls = 0
                    for neighbor in cell:
                        if self.maze[neighbor[0]][neighbor[1]] == 1:
                            walls += 1
                        if self.maze[neighbor[0]][neighbor[1]] == 0:
                            ____.append(neighbor) # dodać do szukania ścian jeżeli jest następna opcja
                    if walls == 3:
                        self.maze[cell[0]][cell[1]] = 1
                        del ____[cell] #usunac z szukania
                        
                for element in ______:
                    to_append =[]
                    if element[1]-1 >= 0:
                        to_append.append((element[0],element[1]-1))
                    if element[0]-1 >= 0:
                        to_append.append((element[0]-1,element[1]))
                    if element[0]+1 < self.rows - 1:
                        to_append.append((element[0]+1,element[1]))
                    if element[1]+1 < self.cols - 1:
                        to_append.append((element[0],element[1]+1))
                    ______ = to_append

running = True
labirynt = Maze(ROWS, COLS,CELL_SIZE)
labirynt.generate_maze()
# keyboard.on_press_key("left", lambda x: labirynt.set_positions("left"))
# keyboard.on_press_key("up", lambda x: labirynt.set_positions("up"))
# keyboard.on_press_key("down", lambda x: labirynt.set_positions("down"))
# keyboard.on_press_key("right", lambda x: labirynt.set_positions("right"))

# labirynt.dfs_solver()
# labirynt.bfs_solver()
labirynt.dead_end_solver()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if labirynt.check_win():
    #     labirynt.end_message()
    #     break
    # else:
    #     labirynt.right_hand_solver()

    pygame.display.update()

pygame.quit()


    # if labirynt.positions != "stay":
    #     labirynt.move_player()

#Right hand 41,41 best time: 3.192 Worst time: 8.84 AVG < 6
#Right hand 75,75 best time: 41.145  Worst time: 52.464 AVG < 
#DFS 41,41 best time: 0.946 Worst time: 2.532 AVG < 2
#DFS 75,75 best time: 5.135 Worst time: 19.599  AVG < 10
#BFS 41,41 best time: 0.098 Worst time: 0.41 AVG < 0.2
#BFS 75,75 best time: 0.898 Worst time: 3.036 AVG < 1.5