from random import shuffle, randrange
import numpy
from numpy.random import randint as rand
from numpy.random import random_integers
import math

class MazeGeneratorAlgo:
    EMPTY = 0       # empty cell
    OBST = 1        # cell with obstacle
    ROBOT = 2       # the position of the robot
    TARGET = 3      # the position of the target


    def getMaze(self):
        return self.grid

    def __init__(self, dimensionRow, dimensionCol,complexity, density):
        """
        Constructor
        """
        self.rows = int(dimensionRow)
        self.columns = int(dimensionCol)
        self.complexity=float(complexity)/100.0
        self.density=float(density)/100.0

        self.robotStart_row = 0  # the initial position of the robot
        self.robotStart_col = 0  # the initial position of the robot        
        self.targetPos_row  = 0  # the position of the target
        self.targetPos_col  = 0  # the position of the target        

        self.grid = [[]]            # the grid
        self.shape = "Square"       # Square is initially selected

        self.array = numpy.array([0] * (self.rows * self.columns))

    def maze(self, width=21, height=21, complexity=.9, density=.1):
        print(width,height,complexity,density)
        # Only odd shapes
        shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
        # Adjust complexity and density relative to maze size
        complexity = int(complexity * (5 * (shape[0] + shape[1]))) # number of components
        density    = int(density * ((shape[0] // 2) * (shape[1] // 2))) # size of components
        # Build actual maze
        Z = numpy.zeros(shape, dtype=int)
        # Fill borders
        Z[0, :] = Z[-1, :] = 1
        Z[:, 0] = Z[:, -1] = 1
        # Make aisles
        for i in range(density):
            x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2 # pick a random position
            Z[y, x] = 1
            for j in range(complexity):
                neighbours = []
                if x > 1:             neighbours.append((y, x - 2))
                if x < shape[1] - 2:  neighbours.append((y, x + 2))
                if y > 1:             neighbours.append((y - 2, x))
                if y < shape[0] - 2:  neighbours.append((y + 2, x))
                if len(neighbours):
                    y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                    if Z[y_, x_] == 0:
                        Z[y_, x_] = 1
                        Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                        x, y = x_, y_
        
        for c in range(self.columns):
            bfound=False
            for r in range(self.rows):
                if Z[c][r] == 0:
                    self.robotStart_col = c
                    self.robotStart_row = r
                    Z[c][r]=2
                    bfound=True
                    break
            if bfound:
                break

        for c in range(self.columns-1,0,-1):
            bfound=False
            for r in range(self.rows-1,0,-1):
                if Z[c][r] == 0:
                    self.targetPos_col = c
                    self.targetPos_row = r
                    Z[c][r]=3
                    bfound=True
                    break
            if bfound:
                break

        return Z

    def createMaze(self):
        """
        Creates a new clean grid or a new maze

        :param make_maze: flag that indicates the creation of a random maze
        """
        self.grid = self.maze(self.columns,self.rows,self.complexity,self.density)


if __name__ == '__main__':
    mg = MazeGeneratorAlgo(9,9,50,50)
    mg.createMaze()
    print(mg.grid)

