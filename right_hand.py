from base_solver import BaseSolver
from typing import Literal

class RightHandSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)
        self.current_direction: Literal["up", "down", "left", "right"] = "left"

    def solve(self):
        while not self.maze.check_win(self.playerX, self.playerY):
            current_rigth = ""
            current_forward = ""
            match self.current_direction:
                case "left":
                    current_rigth = self.maze.matrix[self.playerX - 1][self.playerY]
                    current_forward = self.maze.matrix[self.playerX][self.playerY - 1]
                    if current_rigth != 1:
                        self.playerX -= 1
                        self.current_direction = "up"
                    elif current_forward != 1:
                        self.playerY -= 1
                    else:
                        self.current_direction = "down"
                case "down":
                    current_rigth = self.maze.matrix[self.playerX][self.playerY - 1]
                    current_forward = self.maze.matrix[self.playerX + 1][self.playerY]
                    if current_rigth != 1:
                        self.playerY -= 1
                        self.current_direction = "left"
                    elif current_forward != 1:
                        self.playerX += 1
                    else:
                        self.current_direction = "right"
                case "right":
                    current_rigth = self.maze.matrix[self.playerX + 1][self.playerY]
                    current_forward = self.maze.matrix[self.playerX][self.playerY + 1]
                    if current_rigth != 1:
                        self.playerX += 1
                        self.current_direction = "down"
                    elif current_forward != 1:
                        self.playerY += 1
                    else:
                        self.current_direction = "up"
                case "up":
                    current_rigth = self.maze.matrix[self.playerX][self.playerY + 1]
                    current_forward = self.maze.matrix[self.playerX - 1][self.playerY]
                    if current_rigth != 1:
                        self.playerY += 1
                        self.current_direction = "right"
                    elif current_forward != 1:
                        self.playerX -= 1
                    else:
                        self.current_direction = "left"
            self.maze.draw_maze(self.playerX, self.playerY)
