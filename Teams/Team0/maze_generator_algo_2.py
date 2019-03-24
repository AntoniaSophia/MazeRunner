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

    def __init__(self, dimensionRow, dimensionCol,startCol,startRow,endCol,endRow):
        """
        Constructor
        """
        self.rows = dimensionRow
        self.columns = dimensionCol
        self.robotStart_row = 0  # the initial position of the robot
        self.robotStart_col = 0  # the initial position of the robot        
        self.targetPos_row  = 0  # the position of the target
        self.targetPos_col  = 0  # the position of the target        

        self.grid = [[]]            # the grid
        self.shape = "Square"       # Square is initially selected

        self.array = numpy.array([0] * (dimensionRow * dimensionCol))


    def maze(self, width=21, height=21, complexity=.9, density=.1):
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
        while 1:
            startpos_x = random_integers(0,(width-1)/2)
            startpos_y = random_integers(0,(height-1)/2)
            if Z[startpos_x][startpos_y] == 0:
                Z[startpos_x][startpos_y] = 2
                break
        while 1:
            endpos_x = random_integers((width-1)/2,width-1)
            endpos_y = random_integers((height-1)/2,height-1)
            if Z[endpos_x][endpos_y] == 0:
                Z[endpos_x][endpos_y] = 3
                break
        return Z

    def createMaze(self):
        """
        Creates a new clean grid or a new maze

        :param make_maze: flag that indicates the creation of a random maze
        """
        self.grid = self.maze(self.columns,self.rows,.9,.9)
        numpy.savetxt("c:\\temp\\maze.txt", self.grid, fmt="%d", delimiter=",", newline="\n")
        newgrid=numpy.loadtxt("c:\\temp\\maze.txt", delimiter=',')
        print(newgrid)


if __name__ == '__main__':
    mg = MazeGeneratorAlgo(9,9,0,0,8,8)
    mg.createMaze()

