from maze import Maze

class BaseSolver:
    def __init__(self, maze:Maze) -> None:
        self.maze = maze
        self.playerX = self.maze.startX
        self.playerY = self.maze.startY