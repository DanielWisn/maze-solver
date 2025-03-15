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

class maze:
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

    def draw_maze(self,maze):
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
    
        def backtracking(self,row,col):
            self.maze[row][col] = 0
            self.draw_maze(self.maze)
            
            random.shuffle(self.directions)
            for dx, dy in self.directions:
                new_row, new_col = row + dx * 2, col + dy * 2
                if 1 <= new_row < self.rows-1 and 1 <= new_col < self.cols-1 and self.maze[new_row][new_col] == 1:
                    self.maze[row + dx][col + dy] = 0
                    backtracking(self,new_row,new_col)

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
        if self.check_win() == True:
            self.end_message()
        else:
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

running = True
labirynt = maze(ROWS, COLS,CELL_SIZE)
labirynt.generate_maze()
# keyboard.on_press_key("left", lambda x: labirynt.set_positions("left"))
# keyboard.on_press_key("up", lambda x: labirynt.set_positions("up"))
# keyboard.on_press_key("down", lambda x: labirynt.set_positions("down"))
# keyboard.on_press_key("right", lambda x: labirynt.set_positions("right"))

clock = pygame.time.Clock()  # Add a clock to control FPS

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if labirynt.check_win():
        labirynt.end_message()
        break
    else:
        labirynt.right_hand_solver()

    pygame.display.update()  # Ensure screen updates every frame
    clock.tick(60)  # Limit updates to 10 FPS (adjust as needed)

pygame.quit()


        # if labirynt.positions != "stay":
        #     labirynt.move_player()