import numpy
import math

class MazeSolverAlgo:

    EMPTY = 0       # empty cell
    OBST = 1        # cell with obstacle
    ROBOT = 2       # the position of the robot
    TARGET = 3      # the position of the target

    def __init__(self):
        self.robotStart_col = 0
        self.robotStart_row = 0
        self.targetPos_col = 0
        self.targetPos_row = 0
        self.rows = 0
        self.columns = 0
        print("Initialize a Maze Solver")



    def setDimRows(self, rows):
        self.rows = rows

    def setDimCols(self, cols):
        self.columns = cols

    def setStartCol(self, col):
        self.robotStart_col = col

    def setStartRow(self, row):
        self.robotStart_row = row

    def setEndCol(self, col):
        self.targetPos_col = col

    def setEndRow(self, row):
        self.targetPos_row = row

    def setBlocked(self,col,row):
        self.grid[col][row]=1


    def startMaze(self):
        self.setDimCols = 0 
        self.setDimRows = 0 
        self.setStartCols = 0 
        self.setStartRows = 0 
        self.setEndCols = 0 
        self.setEndRows = 0 
        self.grid=[[]]
    
    def startMaze(self, columns, rows):
        #populate grid with zeros
        self.grid = numpy.empty((rows, columns), dtype=int)
        for i in range(rows):
         for j in range(columns):
             self.grid[i][j]=0

    def endMaze(self):
        self.grid[self.targetPos_row][self.targetPos_col] = self.TARGET
        self.grid[self.robotStart_row][self.robotStart_col] = self.ROBOT

    def printMaze(self):
        print(self.grid)


    def solveMaze(self):
        pass



