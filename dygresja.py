import random

rows = 5
cols = 5

maze = [[1 for _ in range(cols)] for _ in range(rows)]

start_row, start_col = (random.randrange(1, rows, 2), random.randrange(1, cols, 2))
maze[4][4] = 0

print(maze)
