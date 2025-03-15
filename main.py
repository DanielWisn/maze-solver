import pygame
import random
import keyboard
from typing import Literal

ROWS, COLS = 61,61
CELL_SIZE = 10
WIDTH,HEIGHT = ROWS * CELL_SIZE,COLS * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0,255,0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class maze:
    def __init__(self, rows,cols,cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.positions: Literal["up", "down", "left", "right","stay"] = "right"

    def set_positions(self, pos):
        self.positions = pos

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
                pygame.draw.rect(screen, color, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.update()

    def generate_maze(self):
        self.maze = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        start_row, start_col = (random.randrange(1, self.rows-1, 2), random.randrange(1, self.cols-1, 2))
        self.playerX, self.playerY = random.randrange(1, self.rows, 2), self.cols-1
        exit_x, exit_y = random.randrange(1, self.rows, 2), 0
    
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
        self.maze[exit_x][exit_y] = 2
        self.draw_maze(self.maze)
        return maze
    def move_player(self):
        match self.positions:
            case "left":
                if self.playerX == 1:
                    self.playerX = 1
                else:
                    self.playerX -= 1
            case "right":
                if self.playerX == self.rows - 2:
                    self.playerX = self.rows -2
                else:
                    self.playerX += 1

            case "up":
                if self.playerY == 1:
                    self.playerY = 1
                else:
                    self.playerY -= 1
                
            case "down":
                if self.playerY == self.rows - 2:
                    self.playerY = self.rows -2
                else:
                    self.playerY += 1
            case "stay":
                self.playerY = self.playerY
                self.playerX = self.playerX

running = True
labirynt = maze(ROWS, COLS,CELL_SIZE)
labirynt.generate_maze()
keyboard.on_press_key("left", lambda x: labirynt.set_positions("left"))
keyboard.on_press_key("up", lambda x: labirynt.set_positions("up"))
keyboard.on_press_key("down", lambda x: labirynt.set_positions("down"))
keyboard.on_press_key("right", lambda x: labirynt.set_positions("right"))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if labirynt.positions != "stay":
            labirynt.move_player()
            labirynt.draw_maze(labirynt.maze)
pygame.quit()