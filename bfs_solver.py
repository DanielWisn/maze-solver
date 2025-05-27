from base_solver import BaseSolver

class BFSSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)

    def solve(self) -> None:
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
            try:
                next_cell = parents[(next_cell[0],next_cell[1])]
            except:
                self.maze.draw_maze(self.playerX,self.playerY)
                break