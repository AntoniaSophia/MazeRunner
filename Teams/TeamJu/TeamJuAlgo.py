
"""
This class is the template class for the Maze solver
"""

# import sys
# from math import sqrt
# import queue
# import numpy
import os.path


class TeamJuAlgo:

    EMPTY = 0       # empty cell
    OBSTACLE = 1    # cell with obstacle / blocked cell
    START = 2       # the start position of the maze (red color)
    TARGET = 3      # the target/end position of the maze (green color)

    def __init__(self):
        # TODO: this is you job now :-)
        self.master = 0
        self.dimCols = 0
        self.dimRows = 0
        self.startCol = 0
        self.startRow = 0
        self.endCol = 0
        self.endRow = 0
        self.grid = [[]]
        self.came_from = []
        print("\n[TeamJuAlgo]: Constructor TeamJuAlgo successfully executed.")

    # Setter method for the maze dimension of the rows
    def setDimRows(self, rows):
        if rows < 1:
            print("dim < 1 not allowed")
            raise Exception("setDimRows")

        self.dimRows = rows
        

    # Setter method for the maze dimension of the columns
    def setDimCols(self, cols):
        if cols < 1:
            print("cols < 1 not allowed")
            raise Exception("setDimCols")
        self.dimCols = cols
      

    # Setter method for the column of the start position
    def setStartCol(self, col):
        self.startCol = col

    # Setter method for the row of the start position
    def setStartRow(self, row):
        self.startRow = row 

    # Setter method for the column of the end position
    def setEndCol(self, col):
        self.EndCol = col

    # Setter method for the row of the end position
    def setEndRow(self, row):
        self.EndRow = row

    # Setter method for blocked grid elements
    def setBlocked(self, row, col):
        # TODO: this is you job now :-)
        pass

    # Start to build up a new maze
    # HINT: don't forget to initialize all member variables of this class (grid, start position, end position, dimension,...)
    def startMaze(self, columns=0, rows=0):
        # TODO: this is you job now :-)
        pass

    # Start to build up a new maze
    # HINT: don't forget to initialize all member variables of this class (grid, start position, end position, dimension,...)

    # Define what shall happen after the full information of a maze has been received
    def endMaze(self):
        # TODO: this is you job now :-)
        # HINT: did you set start position and end position correctly?
        pass

    # just prints a maze on the command line
    def printMaze(self):
        # TODO: this is you job now :-)
        pass

    # loads a maze from a file pathToConfigFile
    def loadMaze(self, pathToConfigFile):
        # check whether a function numpy.loadtxt() could be useful
        # https://numpy.org/doc/1.20/reference/generated/numpy.loadtxt.html
        # TODO: this is you job now :-)
        exists = os.path.exists(pathToConfigFile)

        if exists:
            print("[TeamJuAlgo]: SUCCESS loading file: ", pathToConfigFile)
        else:
            print("[TeamJuAlgo]: ERROR loading file ", pathToConfigFile)
            return False
    # TODO put loadtxt return into value
    self.grid = np.loadtxt(pathToConfigFile, delimiter=',', dtype='int')
    if len(self.grid.shape) != 2:
        print("Check your maze")
        return False

    # TODO get dimensions of grid
    (self,dimRows, self.dimCols) = self.gridshape

    # TODO get Start pos from grid
    [lstartrowarr, lstartcolarr] = np.where(self.grid == self.START)
    if len(tmp_y_pos) != 1:
        print("Check your Maze")
    self.startRow = tmp_y_pos[0]
    self.startCol = tmp_x_pos[0]

    # TODO get Stop pos from grid
    [lendrowarr, lendcolarr] = np.where(self.grid == self.TARGET)
    self.endRow = tmp_y_pos[0]
    self.endCol = tmp_x_pos[0]

    # clears the complete maze
    def clearMaze(self):
        # TODO: this is you job now :-)
        pass

    # Decides whether a certain row,column grid element is inside the maze or outside
    def isInGrid(self, row, column):
        # TODO: this is you job now :-)
        pass

    # Returns a list of all grid elements neighboured to the grid element row,column
    def getNeighbours(self, row, column):
        # TODO: this is you job now :-)
        # TODO: Add a Unit Test Case --> Very good example for boundary tests and condition coverage
        pass

    # Gives a grid element as string, the result should be a string row,column
    def gridElementToString(self, row, col):
        # TODO: this is you job now :-)
        # HINT: this method is used as primary key in a lookup table
        pass

    # check whether two different grid elements are identical
    # aGrid and bGrid are both elements [row,column]
    def isSameGridElement(self, aGrid, bGrid):
        # TODO: this is you job now :-)
        pass

    # Defines a heuristic method used for A* algorithm
    # aGrid and bGrid are both elements [row,column]

    def heuristic(self, aGrid, bGrid):
        # TODO: this is you job now :-)
        # HINT: a good heuristic could be the distance between to grid elements aGrid and bGrid
        pass

    # Generates the resulting path as string from the came_from list
    def generateResultPath(self, came_from):
        # TODO: this is you job now :-)
        # HINT: this method is a bit tricky as you have to invert the came_from list (follow the path from end to start)
        pass

    def getResultPath(self):
        # TODO: this is you job now :-)
        pass

    #############################
    # Definition of Maze solver algorithm
    #
    # implementation taken from https://www.redblobgames.com/pathfinding/a-star/introduction.html
    #############################
    def myMazeSolver(self):
        # TODO: this is you job now :-)
        pass

    # Command for starting the solving procedure
    def solveMaze(self):
        print("[TeamJuAlgo]: start solving maze... ")
        return self.myMazeSolver()


if __name__ == '__main__':
    mg = TeamJuAlgo()

    # HINT: in case you want to develop the solver without MQTT messages and without always
    #       loading new different mazes --> just load any maze you would like from a file

    mg.loadMaze("..\\..\\MazeExamples\\maze1.txt")
    print("[TeamJuAlgo]: loaded maze", mg.grid)

    # solve the maze
    # HINT: this command shall be received from MQTT client in run_all mode
    solutionString = mg.solveMaze()
    print("[TeamJuAlgo]: Result of solving maze: ", solutionString)
