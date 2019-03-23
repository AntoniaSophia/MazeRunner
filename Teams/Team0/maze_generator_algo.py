from random import shuffle, randrange
import numpy
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

    @staticmethod
    def make_maze(w, h):
        """
        Creates a random, perfect (without cycles) maze
        From http://rosettacode.org/wiki/Maze_generation

        recursive backtracking algorithm

        :param w:   the width of the maze
        :param h:   the height of the maze

        :return:    the maze as a string
        """
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [["| "] * w + ['|'] for _ in range(h)] + [[]]
        hor = [["+-"] * w + ['+'] for _ in range(h + 1)]

        def walk(x, y):
            vis[y][x] = 1

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]:
                    continue
                if xx == x:
                    hor[max(y, yy)][x] = "+ "
                if yy == y:
                    ver[y][max(x, xx)] = "  "
                walk(xx, yy)

        walk(randrange(w), randrange(h))

        s = ""
        for (a, b) in zip(hor, ver):
            s += ''.join(a + b)
        return s

    def createMaze(self):
        """
        Creates a new clean grid or a new maze

        :param make_maze: flag that indicates the creation of a random maze
        """
        # the square maze must have an odd number of rows
        # the rows of the triangular maze must be at least 8 and a multiple of 4
        if (self.rows % 2 != 1 if self.shape == "Square" else self.rows % 4 !=0):
            if self.shape == "Square":
                self.rows -= 1
            else:
                self.rows = max(int(self.rows/4)*4,8)
            
        # the columns of the square maze must be equal to rows
        self.columns = self.rows
        self.grid = self.array[:self.rows*self.columns]
        self.grid = self.grid.reshape(self.rows, self.columns)

        for r in range(self.rows):
            for c in list(range(self.columns)):
                self.grid[r][c] = self.EMPTY

        # start position according to algo
        self.robotStart_row = self.rows-2
        self.robotStart_col = 1

        # target position according to algo
        self.targetPos_row = 1
        self.targetPos_col = self.columns-2

        self.grid[self.targetPos_row][self.targetPos_col] = self.TARGET
        self.grid[self.robotStart_row][self.robotStart_col] = self.ROBOT

        
        maze = self.make_maze(int(self.rows / 2), int(self.columns / 2))
        for r in range(self.rows):
            for c in range(self.columns):
                if maze[r * self.columns + c : r * self.columns + c + 1] in "|-+":
                    self.grid[r][c] = self.OBST


if __name__ == '__main__':
    mg = MazeGeneratorAlgo()
    mg.createMaze()
    mg.printMaze()
