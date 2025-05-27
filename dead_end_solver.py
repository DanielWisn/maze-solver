from base_solver import BaseSolver

class DeadEndSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)

    def solve(self) -> None:
        free_paths = []
        cells_to_check = {}
        path_created = False
        for i in range(0,self.maze.rows):
            for j in range(0,self.maze.cols):
                if self.maze.matrix[i][j] == 0:
                    free_paths.append((i,j))

        while path_created != True:
            for element in free_paths:
                cells_to_check[element] = [(element[0],element[1]-1),(element[0]-1,element[1]),(element[0]+1,element[1]),(element[0],element[1]+1)]

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