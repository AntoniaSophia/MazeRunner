import sys
from math import sqrt
import numpy
import queue

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
        self.dimRows = rows

    def setDimCols(self, cols):
        self.columns = cols
        self.dimColumns = cols

    def setStartCol(self, col):
        self.setStartCols = col

    def setStartRow(self, row):
        self.setStartRows = row

    def setEndCol(self, col):
        self.setEndCols = col

    def setEndRow(self, row):
        self.setEndRows = row

    def setBlocked(self,row ,col):
        self.grid[row][col]=1

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

    def loadMaze(self,pathToConfigFile):
        self.grid=numpy.loadtxt(pathToConfigFile, delimiter=',',dtype=int)
        self.setDimCols=self.grid.shape[0]
        self.setDimRows=self.grid.shape[1]
        start_arr = numpy.where(self.grid == 2)

        self.setStartRows=int(start_arr[0][0])
        self.setStartCols=int(start_arr[1][0])
        end_arr = numpy.where(self.grid == 3)
        self.setEndRows=int(end_arr[0][0])
        self.setEndCols=int(end_arr[1][0])

  
 
    def isInGrid(self,row,column):
        if row < 0:
            return False

        if column < 0:
            return False

        if row >= self.grid.shape[0]:
            return False

        if column >= self.grid.shape[1]:
            return False

        return True


    # TODO: Add a Unit Test Case --> Very good example for boundary tests and condition coverage
    def getNeighbours(self,row,column):
        neighbours = []

        # no neighbours for out-of-grid elements
        if self.isInGrid(row,column) == False:
            return neighbours

        # no neighbours for blocked grid elements
        if self.grid[row,column] == 1:
            return neighbours
    
        nextRow = row + 1    
        if (self.isInGrid(nextRow,column) is True and self.grid[nextRow][column] != 1):
            neighbours.append([nextRow,column])

        previousRow = row - 1    
        if (self.isInGrid(previousRow,column) is True and self.grid[previousRow][column] != 1):
            neighbours.append([previousRow,column])

        nextColumn = column + 1    
        if (self.isInGrid(row,nextColumn) is True and self.grid[row][nextColumn] != 1):
            neighbours.append([row,nextColumn])

        previousColumn = column - 1    
        if (self.isInGrid(row,previousColumn) is True and self.grid[row][previousColumn] != 1):
            neighbours.append([row,previousColumn])

        return neighbours

    #def alreadyVisited(row,column,checkList):


    def gridElementToString(self,row,col):
        result = ""
        result += str(row)
        result += ","
        result += str(col)
        return result
    

    def solveMaze(self):
        result_path=[]
        print("BreadthFirst Solver1")
        print("BreadthFirst Solver2")

        print("Start = " , self.setStartRows , self.setStartCols)
        print("End = " , self.setEndRows , self.setEndCols)
        print("Maze = \n" , self.grid)

#        print("Neighbours [0,4] : " , self.getNeighbours(0,4))

        #############################
        # Here Breadth First starts
        #############################
        start = [self.setStartRows,self.setStartCols]
        frontier = queue.Queue()
        frontier.put(start)
        startKey = self.gridElementToString(self.setStartRows , self.setStartCols)

        came_from = {}
        came_from[startKey] = None
        while not frontier.empty():
            current = frontier.get()

            for next in self.getNeighbours(current[0],current[1]):
                nextKey = self.gridElementToString(next[0] , next[1])
                if nextKey not in came_from:
                    frontier.put(next)
                    came_from[nextKey] = current

        currentKey = self.gridElementToString(self.setEndRows , self.setEndCols)
        path = []
        while currentKey != startKey: 
            path.append(currentKey)
            current = came_from[currentKey]
            currentKey = self.gridElementToString(current[0],current[1])

        path.append(startKey)
        path.reverse()

        #############################
        # Here Breadth First ends
        #############################

        for next in path:
            nextPath = next .split(",")
            result_path.append([int(nextPath[0]),int(nextPath[1])])

        print("Resulting path = " , result_path)

        print("BreadthFirst Solver finished")

        return result_path

if __name__ == '__main__':
    mg = MazeSolverAlgo()
    mg.loadMaze("c:\\temp\\maze2.txt")
   
    for step in  mg.solveMaze():
        step_str = '{},{}'.format(step[0],step[1])
        print(step_str)
