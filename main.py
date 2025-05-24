import pygame
import random
from typing import Literal
import time

ROWS, COLS = 75,75
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
                if self.matrix[row][col] == 0:
                    color = WHITE
                if self.matrix[row][col] == 1:
                    color = BLACK
                if self.matrix[row][col] == 2:
                    color = GREEN
                if self.matrix[row][col] == 3:
                    color = BLUE
                if self.matrix[row][col] == 4:
                    color = RED
                if self.matrix[row][col] == 5:
                    color = PINK
                pygame.draw.rect(screen, color, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.update()
        if dont != True:
             self.matrix[playerX][playerY] = 4

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
        if multiple_paths == True:
            removed_walls = 0
            while removed_walls < 30:
                random_x = random.randrange(2,self.rows-1,2)
                random_y = random.randrange(2,self.cols-1,2)
                neighbor_walls = [(random_x-1,random_y),(random_x+1,random_y),(random_x,random_y-1),(random_x,random_y+1)]
                walls_x, walls_y = 0,0
                if self.matrix[random_x][random_y] == 1:
                    if self.matrix[neighbor_walls[0][0]][neighbor_walls[0][1]] == 1 and self.matrix[neighbor_walls[1][0]][neighbor_walls[1][1]] == 1:
                        walls_x += 2
                    if self.matrix[neighbor_walls[2][0]][neighbor_walls[2][1]] == 1 and self.matrix[neighbor_walls[3][0]][neighbor_walls[3][1]] == 1:
                        walls_y += 2
                    if walls_x == 2 and walls_y == 2:
                        continue
                    elif walls_x == 0 and walls_y == 0:
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


class Solver:
    def __init__(self, maze:Maze) -> None:
        self.maze = maze
        self.playerX = self.maze.startX
        self.playerY = self.maze.startY
        self.current_direction: Literal["up", "down", "left", "right"] = "left"

    def right_hand_solver(self) -> None:
        while self.maze.check_win(self.playerX,self.playerY) != True:
            current_rigth = ""
            current_forward = ""
            match self.current_direction:
                case "left":
                    current_rigth = self.maze.matrix[self.playerX-1][self.playerY]
                    current_forward = self.maze.matrix[self.playerX][self.playerY-1]
                    if current_rigth != 1:
                        self.playerX -= 1
                        self.current_direction = "up"
                    elif current_forward != 1:
                        self.playerY -= 1
                    else:
                        self.current_direction = "down"
                case "down":
                    current_rigth = self.maze.matrix[self.playerX][self.playerY-1]
                    current_forward = self.maze.matrix[self.playerX+1][self.playerY]
                    if current_rigth != 1:
                        self.playerY -= 1
                        self.current_direction = "left"
                    elif current_forward != 1:
                        self.playerX += 1
                    else:
                        self.current_direction = "right"
                case "right":
                    current_rigth = self.maze.matrix[self.playerX+1][self.playerY]
                    current_forward = self.maze.matrix[self.playerX][self.playerY+1]
                    if current_rigth != 1:
                        self.playerX += 1
                        self.current_direction = "down"
                    elif current_forward != 1:
                        self.playerY += 1
                    else:
                        self.current_direction ="up"
                case "up":
                    current_rigth = self.maze.matrix[self.playerX][self.playerY+1]
                    current_forward = self.maze.matrix[self.playerX-1][self.playerY]
                    if current_rigth != 1:
                        self.playerY += 1
                        self.current_direction = "right" 
                    elif current_forward != 1:
                        self.playerX-= 1
                    else:
                        self.current_direction = "left"

            self.maze.draw_maze(self.playerX,self.playerY)

    def dfs_solver(self) -> None:
        stack = []
        neighbors = [(self.playerX,self.playerY-1)]
        while self.maze.check_win(self.playerX,self.playerY) != True:
            options = []
            for neighbor in neighbors:
                if self.maze.matrix[neighbor[0]][neighbor[1]] == 0 or self.maze.matrix[neighbor[0]][neighbor[1]] == 2:
                    options.append(neighbor)
            if len(options) > 1:
                stack.append((self.playerX,self.playerY))
                self.playerX,self.playerY = options[0][0],options[0][1]
                
            if len(options) == 1:
                self.playerX,self.playerY = options[0][0],options[0][1]
            
            if len(options) == 0:
                self.playerX,self.playerY = stack[-1][0],stack[-1][1]
                stack.pop(-1)

            neighbors = [(self.playerX,self.playerY-1),(self.playerX-1,self.playerY),(self.playerX+1,self.playerY),(self.playerX,self.playerY+1)]
            self.maze.draw_maze(self.playerX,self.playerY)
    
    def bfs_solver(self) -> None:
        queue = []
        parents = {}
        neighbors = [(self.playerX,self.playerY-1,(self.playerX,self.playerY))]
        while self.maze.check_win(self.playerX,self.playerY) != True:
            for neighbor in neighbors:
                if self.maze.matrix[neighbor[0]][neighbor[1]] == 0:
                    queue.append(neighbor)
                    parents[(neighbor[0],neighbor[1])] = neighbor[2]
                    self.maze.matrix[neighbor[0]][neighbor[1]] = 4
                if self.maze.matrix[neighbor[0]][neighbor[1]] == 2:
                    parents[(neighbor[0],neighbor[1])] = neighbor[2]
                    self.playerX,self.playerY = neighbor[0],neighbor[1]
            
            neighbors = []
            for element in queue:
                neighbors.extend([(element[0],element[1]-1,(element[0],element[1])),(element[0]-1,element[1],(element[0],element[1])),(element[0]+1,element[1],(element[0],element[1])),(element[0],element[1]+1,(element[0],element[1]))])

            queue.pop(0)
            self.maze.draw_maze(self.playerX,self.playerY)
        
        shortest_path_created = False
        next_cell = parents[(self.playerX,self.playerY)]
        while not shortest_path_created:
            self.maze.matrix[next_cell[0]][next_cell[1]] = 2
            self.maze.draw_maze(self.playerX,self.playerY)
            try:
                next_cell = parents[(next_cell[0],next_cell[1])]
            except:
                break
        
    def dead_end_solver(self) -> None:
        free_paths = []
        cells_to_check = {}
        path_created = False
        for i in range(0,self.maze.rows):
            for j in range(0,self.maze.cols):
                if self.maze.matrix[i][j] == 0:
                    free_paths.append((i,j))

        while path_created != True:
            for element in free_paths:
                to_append = []
                to_append.extend([(element[0],element[1]-1),(element[0]-1,element[1]),(element[0]+1,element[1]),(element[0],element[1]+1)])
                cells_to_check[element] = to_append
            to_delete = []
            for cell in cells_to_check:
                walls = 0
                for neighbor in cells_to_check[cell]:
                    if self.maze.matrix[neighbor[0]][neighbor[1]] == 1:
                        walls += 1

                if walls == 3:
                    self.maze.matrix[cell[0]][cell[1]] = 1
                    to_delete.append((cell[0],cell[1]))
                    self.maze.draw_maze(self.playerX,self.playerY)

            if not to_delete:
                path_created = True
                self.finished = True
                for i in free_paths:
                    self.maze.matrix[i[0]][i[1]] = 2
                self.maze.draw_maze(self.playerX,self.playerY)
                self.maze.check_win(self.playerX,self.playerY)


            for i in to_delete:
                free_paths.remove(i)
                cells_to_check.pop(i)
        
    def tremaux_solver(self) -> None:
        self.dont = True
        self.playerX,self.playerY = self.playerX,self.playerY-1
        neighbors = [(self.playerX,self.playerY-1),(self.playerX-1,self.playerY),(self.playerX+1,self.playerY),(self.playerX,self.playerY+1)]
        stack = []
        while self.maze.check_win(self.playerX,self.playerY) != True:
            free_paths = 0
            next_move = ()
            decision_made = False
            for neighbor in neighbors:
                if self.maze.matrix[self.playerX][self.playerY-1] == 2:
                    self.maze.matrix[self.playerX][self.playerY] = 5
                    self.playerY -= 1
                    next_move = True
                    decision_made = True
                if self.maze.matrix[neighbor[0]][neighbor[1]] == 0 or self.maze.matrix[neighbor[0]][neighbor[1]] == 2 and next_move == ():
                    next_move = (neighbor[0],neighbor[1],1)
                    free_paths += 1
                if self.maze.matrix[neighbor[0]][neighbor[1]] == 5 and next_move == ():
                    next_move = (neighbor[0],neighbor[1],2)
                    free_paths += 1

            if free_paths >= 3:
                stack.append((self.playerX,self.playerY))
            
            if next_move == () and decision_made == False:
                self.maze.matrix[self.playerX][self.playerY] = 4
                self.playerX,self.playerY = stack[-1][0],stack[-1][1]
                print("cofam")
                del stack[-1]
                decision_made = True
            print(next_move)

            if next_move[2] == 1 and decision_made == False:
                self.maze.matrix[self.playerX][self.playerY] = 5
                self.playerX,self.playerY = next_move[0],next_move[1]
                decision_made = True

            if next_move[2] == 2 and decision_made == False:
                self.maze.matrix[self.playerX][self.playerY] = 4
                self.playerX,self.playerY = next_move[0],next_move[1]
                decision_made = True
                
            self.maze.draw_maze(self.playerX,self.playerY,True)
            neighbors = [(self.playerX,self.playerY-1),(self.playerX-1,self.playerY),(self.playerX+1,self.playerY),(self.playerX,self.playerY+1)]

    def a_star(self) -> None:
        class PriorityQueue:
            def __init__(self, startX, startY, exitX, exitY) -> None:
                self.goalX = exitX
                self.goalY = exitY
                self.path = {} 
                self.path_cost = {(startX, startY): 0}
                self.to_explore = [((startX, startY), self.heuristic((startX, startY)))]

            def heuristic(self, node: tuple) -> int:
                return abs(node[0] - self.goalX) + abs(node[1] - self.goalY)

            def add_element(self, node: tuple):
                x, y, parent = node[0], node[1], node[2]
                current = (x, y)

                self.path_cost[current] = self.path_cost.get(parent, 0) + 1

                f_score = self.path_cost[current] + self.heuristic(current)

                self.to_explore.append((current, f_score))

                self.path[current] = parent

                index = len(self.to_explore) - 1
                while index > 0:
                    parent_index = (index - 1) // 2
                    if self.to_explore[index][1] < self.to_explore[parent_index][1]:
                        self.to_explore[index], self.to_explore[parent_index] = self.to_explore[parent_index], self.to_explore[index]
                        index = parent_index
                    else:
                        break

            def bubble_down(self, index: int):
                size = len(self.to_explore)
                while True:
                    smallest = index
                    left = 2 * index + 1
                    right = 2 * index + 2

                    if left < size and self.to_explore[left][1] < self.to_explore[smallest][1]:
                        smallest = left

                    if right < size and self.to_explore[right][1] < self.to_explore[smallest][1]:
                        smallest = right

                    if smallest != index:
                        self.to_explore[index], self.to_explore[smallest] = self.to_explore[smallest], self.to_explore[index]
                        index = smallest
                    else:
                        break

        self.maze.matrix[self.playerX][self.playerY] = 1
        self.playerY-=1
        queue = PriorityQueue(self.playerX,self.playerY,self.maze.exitX,self.maze.exitY)
        neighbors = [(self.playerX,self.playerY-1),(self.playerX-1,self.playerY),(self.playerX+1,self.playerY),(self.playerX,self.playerY+1)]
        for i in neighbors:
            neighbor_cost = queue.path_cost[(self.playerX,self.playerY)] + 1
            if self.maze.matrix[i[0]][i[1]] == 1:
                    continue
            if (i[0],i[1]) not in queue.path_cost or queue.path_cost[(i[0],i[1])] > neighbor_cost:
                queue.add_element((i[0],i[1],(self.playerX,self.playerY)))
                self.maze.matrix[i[0]][i[1]] = 4

        self.maze.matrix[self.playerX][self.playerY] = 3
        self.maze.draw_maze(self.playerX,self.playerY,True)
        visited = set()
        while len(queue.to_explore) != 0:
            self.maze.draw_maze(self.playerX,self.playerY,True)
            current_node = queue.to_explore[0]
            current_node = current_node[0]
            if len(queue.to_explore) == 1:
                queue.to_explore.pop()
            else:
                queue.to_explore[0] = queue.to_explore.pop()
                queue.bubble_down(0)
            
            if current_node in visited:
                continue
            visited.add(current_node)

            neighbors = [(current_node[0],current_node[1]-1),(current_node[0]-1,current_node[1]),(current_node[0]+1,current_node[1]),(current_node[0],current_node[1]+1)]
            if current_node == (self.maze.exitX,self.maze.exitY):
                next_cell = queue.path[current_node]
                self.playerX,self.playerY = current_node[0],current_node[1]
                self.maze.check_win(self.playerX,self.playerY)
                while next_cell in queue.path:
                    self.maze.matrix[next_cell[0]][next_cell[1]] = 2
                    self.maze.draw_maze(self.playerX, self.playerY, True)
                    next_cell = queue.path[next_cell]
                break
            
            for i in neighbors:
                neighbor_cost = queue.path_cost[current_node] + 1
                if self.maze.matrix[i[0]][i[1]] == 1:
                    continue
                if (i[0],i[1]) not in queue.path_cost or queue.path_cost[(i[0],i[1])] > neighbor_cost:
                    queue.add_element((i[0],i[1],current_node))
                    self.maze.matrix[i[0]][i[1]] = 4



running = True
labirynt = Maze(ROWS, COLS,CELL_SIZE)
labirynt.generate_maze()
solver = Solver(labirynt)

# solver.right_hand_solver()
# solver.dfs_solver()
# solver.bfs_solver()
# solver.dead_end_solver()
# solver.tremaux_solver()
solver.a_star()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()

#Right hand 41,41 best time: 3.192 Worst time: 8.84 AVG < 6
#Right hand 75,75 best time: 41.145  Worst time: 52.464 AVG < 
#DFS 41,41 best time: 0.946 Worst time: 2.532 AVG < 2
#DFS 75,75 best time: 5.135 Worst time: 19.599  AVG < 10
#BFS 41,41 best time: 0.098 Worst time: 0.41 AVG < 0.2
#BFS 75,75 best time: 0.898 Worst time: 3.036 AVG < 1.5
#DEAD 41,41 AVG < 0.55
#DEAD 75,75 AVG < 6
#Tremaux 41,41 Best:0.209 Worst:1.11 AVG < 0.9
#Tremaux 75,75 Best:4.334 Worst: 12,823 AVG < 10
#A* 41,41
#A* 75,75 Best: 2,925 Worst: 6.641