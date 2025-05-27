from base_solver import BaseSolver

class AStarSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)

    def solve(self) -> None:
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
        self.maze.matrix[self.playerX][self.playerY] = 3

        while len(queue.to_explore) != 0:
            self.maze.draw_maze(self.playerX,self.playerY,True)
            current_node = queue.to_explore[0]
            current_node = current_node[0]
            
            if len(queue.to_explore) == 1:
                queue.to_explore.pop()
            else:
                queue.to_explore[0] = queue.to_explore.pop()
                queue.bubble_down(0)

            neighbors = [(current_node[0],current_node[1]-1),(current_node[0]-1,current_node[1]),(current_node[0]+1,current_node[1]),(current_node[0],current_node[1]+1)]
            if current_node == (self.maze.exitX,self.maze.exitY):
                next_cell = queue.path[current_node]
                self.playerX,self.playerY = current_node[0],current_node[1]
                self.maze.check_win(self.playerX,self.playerY)
                while next_cell in queue.path:
                    self.maze.matrix[next_cell[0]][next_cell[1]] = 2
                    next_cell = queue.path[next_cell]

                self.maze.draw_maze(self.playerX, self.playerY, True)
                break
            
            for i in neighbors:
                neighbor_cost = queue.path_cost[current_node] + 1
                if self.maze.matrix[i[0]][i[1]] == 1:
                    continue
                if (i[0],i[1]) not in queue.path_cost or queue.path_cost[(i[0],i[1])] > neighbor_cost:
                    queue.add_element((i[0],i[1],current_node))
                    self.maze.matrix[i[0]][i[1]] = 4
