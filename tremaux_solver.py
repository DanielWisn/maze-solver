from base_solver import BaseSolver

class TremauxSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)

    def solve(self) -> None:
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
                del stack[-1]
                decision_made = True

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