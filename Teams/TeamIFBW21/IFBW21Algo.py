"""
Susannas implementation of AStar done during exercise
"""

# import sys
# from math import sqrt
import queue
import numpy as np
import os.path


class IFBW21Algo:

    EMPTY = 0       # empty cell
    BLOCKED = 1    # cell with obstacle / blocked cell
    START = 2       # the start position of the maze (red color)
    END = 3      # the target/end position of the maze (green color)

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
        print("\n[IFBW21Algo]: Constructor IFBW21Algo successfully executed.")

    # Setter method for the maze dimension of the rows
    def setDimRows(self, rows):
        if rows < 1:
            print("dim < 1 not allowed")
            raise Exception("setDimRows")
        self.dimRows = rows

    # Setter method for the maze dimension of the columns
    def setDimCols(self, cols):
        if cols < 1:
            print("dim < 1 not allowed")
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
        self.endCol = col

    # Setter method for the row of the end position
    def setEndRow(self, row):
        self.endRow = row

    # Setter method for blocked grid elements
    def setBlocked(self, row, col):
        self.grid[row, col] = self.BLOCKED

    # Start to build up a new maze
    # HINT: don't forget to initialize all member variables of this class (grid, start position, end position, dimension,...)
    def startMaze(self):
        if self.dimRows == 0 or self.dimCols == 0:
            return
        self.grid = np.zeros((self.dimRows, self.dimCols), dtype='int')

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
        exists = os.path.exists(pathToConfigFile)

        if not exists:
            print("[IFBW21Algo]: ERROR loading file ", pathToConfigFile)
            return False

        print("[IFBW21Algo]: SUCCESS loading file ", pathToConfigFile)

        # put loadtxt return into value
        self.grid = np.loadtxt(pathToConfigFile, delimiter=',', dtype='int')

        if len(self.grid.shape) != 2:
            print("[IFBW21Algo]: Check your Maze!")
            return False

        # get dimension of grid
        (ldimRows, ldimCols) = self.grid.shape
        self.setDimRows(ldimRows)
        self.setDimCols(ldimCols)

        # get Start pos from grid
        [lStartRowArr, lStartColArr] = np.where(self.grid == self.START)
        if len(lStartRowArr) != 1 or len(lStartColArr) != 1:
            print("[IFBW21Algo]: Check the start pos of the Maze!")
            return False

        self.setStartRow(lStartRowArr[0])
        self.setStartCol(lStartColArr[0])

        # get End pos from grid
        [lEndRowArr, lEndColArr] = np.where(self.grid == self.END)
        if len(lEndRowArr) != 1 or len(lEndColArr) != 1:
            print("[IFBW21Algo]: Check the end pos of the Maze!")
            return False

        self.setEndRow(lEndRowArr[0])
        self.setEndCol(lEndColArr[0])

        return True

    # clears the complete maze
    def clearMaze(self):
        # TODO: this is you job now :-)
        pass

    # Decides whether a certain row,column grid element is inside the maze or outside
    def isInGrid(self, row, column):
        if row < 0 or row >= self.dimRows or column < 0 or column >= self.dimCols:
            return False
        return True

    # Returns a list of all grid elements neighboured to the grid element row,column
    def getNeighboursArr(self, arrpos):
        return self.getNeighbours(arrpos[0], arrpos[1])

    def getNeighbours(self, row, column):
        lNeighbours = []
        if not self.isInGrid(row, column):
            return False

        directions = [(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1)]
        for direction in directions:
            if self.isInGrid(direction[0], direction[1]) and self.grid[direction[0], direction[1]] != self.BLOCKED:
                lNeighbours.append(direction)

        return lNeighbours

    # Gives a grid element as string, the result should be a string row,column
    def gridElementToString(self, row, col):
        return f'{row}-{col}'

    # check whether two different grid elements are identical
    # aGrid and bGrid are both elements [row,column]
    def isSameGridElement(self, aGrid, bGrid):
        return aGrid == bGrid

    # Defines a heuristic method used for A* algorithm
    # aGrid and bGrid are both elements [row,column]
    def heuristic(self, aGrid, bGrid):
        # Manhattan distance on a square grid
        # taken from https://www.redblobgames.com/pathfinding/a-star/introduction.html
        return abs(aGrid[0] - bGrid[0]) + abs(aGrid[1] - bGrid[1])

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
        frontier = queue.PriorityQueue()
        start = (self.startRow, self.startCol)
        frontier.put((0, start))
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0

        goal = (self.endRow, self.endCol)

        while not frontier.empty():
            current = frontier.get()[1]
            if current == goal:
                break
            for next in self.getNeighbours(current[0], current[1]):
                new_cost = cost_so_far[current] + 1  # Simplified costs

                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic([self.endRow, self.endCol], next)
                    frontier.put((priority, next))
                    came_from[next] = current

        self.came_from = came_from
        self.solution_path = self.getSolvePath(came_from)
        return self.solution_path

    def getSolvePath(self, came_from):
        current = (self.endRow, self.endCol)
        start = (self.startRow, self.startCol)
        path = []
        while not self.isSameGridElement(current, start):
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path

    # Command for starting the solving procedure
    def solveMaze(self):
        print("[IFBW21Algo]: start solving maze... ")
        return self.myMazeSolver()


if __name__ == '__main__':
    mg = IFBW21Algo()

    # HINT: in case you want to develop the solver without MQTT messages and without always
    #       loading new different mazes --> just load any maze you would like from a file

    mg.loadMaze("..\\..\\MazeExamples\\maze1_solvetest.txt")
    print("[IFBW21Algo]: loaded maze\n", mg.grid)

    # solve the maze
    # HINT: this command shall be received from MQTT client in run_all mode
    solvepath = mg.solveMaze()
    print("[IFBW21Algo]: Result of solving maze: ", str(solvepath))
