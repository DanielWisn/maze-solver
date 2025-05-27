from base_solver import BaseSolver

class DFSSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)

    def solve(self) -> None:
        stack = []
        parents = {}
        neighbors = [(self.playerX,self.playerY-1)]
        while self.maze.check_win(self.playerX,self.playerY) != True:
            options = []
            for neighbor in neighbors:
                if self.maze.matrix[neighbor[0]][neighbor[1]] == 0 or self.maze.matrix[neighbor[0]][neighbor[1]] == 2:
                    options.append(neighbor)
                    parents[neighbor] = (self.playerX,self.playerY)

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

        next_cell = parents[(self.playerX,self.playerY)]
        while True:
            self.maze.matrix[next_cell[0]][next_cell[1]] = 2
            try:
                next_cell = parents[(next_cell[0],next_cell[1])]
            except:
                self.maze.draw_maze(self.playerX,self.playerY)
                break