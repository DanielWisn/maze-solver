from right_hand import RightHandSolver
from dfs_solver import DFSSolver
from bfs_solver import BFSSolver
from dead_end_solver import DeadEndSolver
from tremaux_solver import TremauxSolver
from a_star_solver import AStarSolver
from maze import Maze
import pygame

ROWS, COLS = 45,45
CELL_SIZE = 10
WIDTH,HEIGHT = ROWS * CELL_SIZE,COLS * CELL_SIZE
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


running = True
maze = Maze(ROWS, COLS,CELL_SIZE)
maze.generate_maze()

# solver = RightHandSolver(maze)
# solver = DFSSolver(maze)
# solver = BFSSolver(maze)
solver = DeadEndSolver(maze)
# solver = TremauxSolver(maze)
# solver = AStarSolver(maze)

solver.solve()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
