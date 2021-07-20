
"""
This class is the template class for the Maze solver
"""

# import sys
# from math import sqrt
# import queue
import numpy
import os.path
from queue import PriorityQueue


class SusannaAStarAlgo:

    EMPTY = 0       # empty cell
    OBSTACLE = 1    # cell with obstacle / blocked cell
    START = 2       # the start position of the maze (red color)
    TARGET = 3      # the target/end position of the maze (green color)

    def __init__(self):
        # TODO: this is you job now :-)
        self.dimCols = 0
        self.dimRows = 0
        self.startCol = 0
        self.startRow = 0
        self.endCol = 0
        self.endRow = 0
        self.grid = [[]]
        self.resultpath = []
        print("\n[TeamTemplateAlgo]: Constructor TeamTemplateAlgo successfully executed.")

    # Setter method for the maze dimension of the rows
    def setDimRows(self, rows):
        self.dimRows=rows

    # Setter method for the maze dimension of the columns
    def setDimCols(self, cols):
        self.dimCols=cols

    # Setter method for the column of the start position
    def setStartCol(self, col):
        self.startCol=col

    # Setter method for the row of the start position
    def setStartRow(self, row):
        self.startRow=row

    # Setter method for the column of the end position
    def setEndCol(self, col):
        self.endCol=col

    # Setter method for the row of the end position
    def setEndRow(self, row):
        self.EndRow=row

    # Setter method for blocked grid elements
    def setBlocked(self, row, col):
        self.grid[row][col]=self.OBSTACLE

    # Start to build up a new maze
    # HINT: don't forget to initialize all member variables of this class (grid, start position, end position, dimension,...)
    def startMaze(self, columns=0, rows=0):
        if rows > 0:
            self.dimRows = rows

        if columns > 0:
            self.dimCols = columns

        if columns == 0 and rows == 0:
            self.dimRows = 0
            self.dimCols = 0

        self.startCols = 0
        self.startRows = 0
        self.endCols = 0
        self.endRows = 0
        self.grid = [[]]
        
        # self.grid = numpy.empty((self.dimCols, self.dimRows), dtype=int)

        for row in range(self.dimRows):
            for col in range(self.dimCols):
                self.grid[row][col]=self.EMPTY
    
    # Define what shall happen after the full information of a maze has been received
    def endMaze(self):
        self.grid[self.startRow][self.startCol] = self.START
        self.grid[self.endRow][self.endCol] = self.TARGET

    # just prints a maze on the command line
    def printMaze(self):
        print(self.grid)

    # loads a maze from a file pathToConfigFile
    def loadMaze(self, pathToConfigFile) -> bool:
        # check whether a function numpy.loadtxt() could be useful
        # https://numpy.org/doc/1.20/reference/generated/numpy.loadtxt.html
        exists = os.path.exists(pathToConfigFile)

        if exists:
            print("[TeamTemplateAlgo]: SUCCESS file exist: ", pathToConfigFile)
        else:
            print("[TeamTemplateAlgo]: ERROR file not exist ", pathToConfigFile)
            return False
        
        try:

            self.grid=numpy.loadtxt(pathToConfigFile, dtype='int64',delimiter=",")
            (self.dimRows,self.dimCols)=self.grid.shape
            ypos=0

            [self.endRow,self.endCol] = numpy.concatenate(numpy.where(self.grid==self.TARGET)).tolist()
            [self.startRow,self.startCol] = numpy.concatenate(numpy.where(self.grid==self.START)).tolist()
            
            # # This can be solved much easier or?!
            # for ypos in range(self.dimRows):
            #     for xpos in range(self.dimCols):
            #         if int(self.grid[ypos][xpos])==self.TARGET:
            #             self.endRow=ypos
            #             self.endCol=xpos
            #         elif int(self.grid[ypos][xpos])==self.START:
            #             self.startRow=ypos
            #             self.startCol=xpos
                       
        except ValueError as err:
            print(f"Error in Maze please check: {err}",pathToConfigFile)
            return False
        return True

    # clears the complete maze
    def clearMaze(self):
        self.startMaze()


    # Decides whether a certain row,column grid element is inside the maze or outside
    def isInGrid(self, row, column):
        if row<0 or row>=self.dimRows or column <0 or column>=self.dimCols:
            return False
        return True

    # Returns a list of all grid elements neighboured to the grid element row,column

    def getNeighbours(self, row, column):
        neighbours=[]
        
        if not self.isInGrid(row,column):
            return neighbours

        # left
        if self.isInGrid(row,column-1) and self.grid[row][column-1]!= self.OBSTACLE:
            neighbours.append((row,column-1))
        # up
        if self.isInGrid(row-1,column) and self.grid[row-1][column]!= self.OBSTACLE:
            neighbours.append((row-1,column))
        # down
        if self.isInGrid(row+1,column) and self.grid[row+1][column]!= self.OBSTACLE:
            neighbours.append((row+1,column))
        # right
        if self.isInGrid(row,column+1) and self.grid[row][column+1]!= self.OBSTACLE:
            neighbours.append((row,column+1))

        return neighbours

    # return a grid element as string, the result should be a string "<row>,<column>"
    def gridElementToString(self, row, col) -> str:
        return '{},{}'.format(row, col)

    # check whether two different grid elements are identical
    # aGrid and bGrid are both elements [row,column]
    def isSameGridElement(self, aGrid, bGrid):
        return aGrid==bGrid
        # if aGrid[0] == bGrid[0] and aGrid[1]==bGrid[1]:
        #     return True
        # else:
        #     return False

    # Defines a heuristic method used for A* algorithm
    # aGrid and bGrid are both elements [row,column]

    def heuristic(self, aGrid, bGrid):
        return numpy.linalg.norm(numpy.array(aGrid)-numpy.array(bGrid))

    # Generates the resulting path as string from the came_from list
    def generateResultPath(self, came_from):
        mazepath=[]
        # while 1:
        mazepath.append((self.endRow,self.endCol))
        nextmove=came_from[(self.endRow,self.endCol)]
        mazepath.insert(0,nextmove)

        while not self.isSameGridElement(nextmove,(self.startRow,self.startCol)):
           nextmove = came_from[nextmove]
           mazepath.insert(0,nextmove)

        self.resultpath=mazepath
        return mazepath

    #############################
    # Definition of Maze solver algorithm
    #
    # implementation taken from https://www.redblobgames.com/pathfinding/a-star/introduction.html
    #############################
    def myMazeSolver(self):
        print(self.startRow,"-",self.startCol)
        frontier = PriorityQueue()
        frontier.put((self.startRow,self.startCol),0)
        came_from = dict()
        cost_so_far = dict()

        came_from[(self.startRow,self.startCol)] = None
        cost_so_far[(self.startRow,self.startCol)] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == (self.endRow,self.endCol):
                break
            for nextfrontier in self.getNeighbours(current[0],current[1]):
                new_cost = cost_so_far[current] + 1 # Cost set to 1
                if nextfrontier not in cost_so_far or new_cost < cost_so_far[nextfrontier]:
                    cost_so_far[nextfrontier] = new_cost
                    priority = new_cost + self.heuristic((self.endRow,self.endCol), nextfrontier)
                    frontier.put(nextfrontier, priority)
                    came_from[nextfrontier] = current
       
        return  self.generateResultPath(came_from)

    # Command for starting the solving procedure
    def solveMaze(self):
        print("[TeamTemplateAlgo]: start solving maze... ")
        return self.myMazeSolver()


if __name__ == '__main__':
    mg = SusannaAStarAlgo()

    # HINT: in case you want to develop the solver without MQTT messages and without always
    #       loading new different mazes --> just load any maze you would like from a file

    if not mg.loadMaze("..\\..\\MazeExamples\\Maze1.txt"):
        exit(1)

    print("[TeamTemplateAlgo]: loaded maze\n", mg.grid)
    # solve the maze
    # HINT: this command shall be received from MQTT client in run_all mode

    solutionString = mg.solveMaze()
    print("[TeamTemplateAlgo]: Result of solving maze: ", solutionString)
