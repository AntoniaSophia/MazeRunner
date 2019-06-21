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
        self.grid[self.setEndRows][self.setEndCols] = self.TARGET
        self.grid[self.setStartRows][self.setStartCols] = self.ROBOT

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

    def clearMaze(self):
        self.startMaze()
  
 
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


    def gridElementToString(self,row,col):
        result = ""
        result += str(row)
        result += ","
        result += str(col)
        return result
    
    def isSameGridElement(self, aGrid, bGrid):
        if (aGrid[0] == bGrid[0] and aGrid[1] == bGrid[1]):
            return True

        return False

    def heuristic(self, aGrid, bGrid):
        return abs(aGrid[0] - bGrid[0]) + abs(aGrid[1] - bGrid[1])


    #############################
    # Definition of BreadthFirst algorithm
    #############################
    def breadthFirst(self):
        result_path=[]
        print("Start of BreadthFirst Solver...")

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

        #############################
        # Here Breadth First ends
        #############################

        #############################
        # Here Creation of Path starts
        #############################
        currentKey = self.gridElementToString(self.setEndRows , self.setEndCols)
        path = []
        while currentKey != startKey: 
            path.append(currentKey)
            current = came_from[currentKey]
            currentKey = self.gridElementToString(current[0],current[1])

        path.append(startKey)
        path.reverse()
        #############################
        # Here Creation of Path ends
        #############################

        for next in path:
            nextPath = next .split(",")
            result_path.append([int(nextPath[0]),int(nextPath[1])])

        print("Resulting length BreadthFirst Solution: " , len(result_path))
        print("Resulting BreadthFirst Solution Path = " , result_path)

        print("Finished BreadthFirst Solver....")

        return result_path

    #############################
    # Definition of A* algorithm
    #############################
    def aStar(self):
        result_path=[]
        print("Start of A* Solver...")

        print("Start = " , self.setStartRows , self.setStartCols)
        print("End = " , self.setEndRows , self.setEndCols)
        print("Maze = \n" , self.grid)

#        print("Neighbours [0,4] : " , self.getNeighbours(0,4))

        #############################
        # Here A* starts
        #############################
        start = [self.setStartRows,self.setStartCols]
        frontier = queue.PriorityQueue()
        frontier.put((0,start))
        #frontier.put(start,0)

        startKey = self.gridElementToString(self.setStartRows , self.setStartCols)
        came_from = {}
        came_from[startKey] = None

        cost_so_far = {}
        cost_so_far[startKey] = 0

        goal = [self.setEndRows , self.setEndCols]
        
        while not frontier.empty():
            current = frontier.get()[1]
            currentKey = self.gridElementToString(current[0] , current[1])
            #print("First Queue Element = " , currentKey)

            if self.isSameGridElement(current,goal):
                break

            for next in self.getNeighbours(current[0],current[1]):
                new_cost =  cost_so_far[currentKey] + 1     # + 1 is extremely important, otherwise you would not punish additional moves!!!
                                                            # +1 = graph costs

                nextKey = self.gridElementToString(next[0] , next[1])
                if nextKey not in cost_so_far or new_cost < cost_so_far[nextKey]:
                    cost_so_far[nextKey] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    #print("Next = " , nextKey , " - priority = " , priority)
                    frontier.put((priority,next))
                    came_from[nextKey] = current            
        #############################
        # Here A* ends
        #############################


        #############################
        # Here Creation of Path starts
        #############################
        currentKey = self.gridElementToString(self.setEndRows , self.setEndCols)
        path = []
        while currentKey != startKey: 
            path.append(currentKey)
            current = came_from[currentKey]
            currentKey = self.gridElementToString(current[0],current[1])

        path.append(startKey)
        path.reverse()
        #############################
        # Here Creation of Path ends
        #############################
        for next in path:
            nextPath = next .split(",")
            result_path.append([int(nextPath[0]),int(nextPath[1])])

        print("Resulting length A* Solution: " , len(result_path))
        print("Resulting A* Solution Path = " , result_path)

        print("Finished A* Solver....")

        return result_path


    def solveMaze(self):
        #return self.breadthFirst()
        return self.aStar()

if __name__ == '__main__':
    mg = MazeSolverAlgo()
    mg.loadMaze("c:\\temp\\maze1.txt")
   
    for step in  mg.solveMaze():
        step_str = '{},{}'.format(step[0],step[1])
        #print(step_str)
