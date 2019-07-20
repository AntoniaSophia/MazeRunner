import sys
from math import sqrt
import numpy
import queue

class MazeSolverAlgo:

    EMPTY = 0       # empty cell
    OBSTACLE = 1    # cell with obstacle
    START = 2       # the position of the robot
    TARGET = 3      # the position of the target

    def __init__(self):
        self.rows = 0
        self.columns = 0
        print("Initialize a Maze Solver")

    def setDimRowsCmd(self, rows):
        self.rows = rows
        self.dimRows = rows

    def setDimColsCmd(self, cols):
        self.columns = cols
        self.dimColumns = cols

    def setStartColCmd(self, col):
        self.setStartCol = col

    def setStartRowCmd(self, row):
        self.setStartRow = row

    def setEndColCmd(self, col):
        self.setEndCol = col

    def setEndRowCmd(self, row):
        self.setEndRow = row

    def setBlocked(self,row ,col):
        self.grid[row][col] = self.OBSTACLE

    def startMaze(self, columns=0, rows=0):
        self.dimCols = 0 
        self.dimRows = 0 
        self.setStartCols = 0 
        self.setStartRows = 0 
        self.setEndCols = 0 
        self.setEndRows = 0 
        self.grid=[[]]        

        if columns>0 and rows>0:
            self.grid = numpy.empty((rows, columns), dtype=int)
            for i in range(rows):
                for j in range(columns):
                    self.grid[i][j]=0

    def endMaze(self):
        self.grid[self.setStartRow][self.setStartCol] = self.START
        self.grid[self.setEndRow][self.setEndCol] = self.TARGET

    def printMaze(self):
        print(self.grid)

    def loadMaze(self,pathToConfigFile):
        self.grid=numpy.loadtxt(pathToConfigFile, delimiter=',',dtype=int)
        self.setDimCols=self.grid.shape[0]
        self.setDimRows=self.grid.shape[1]

        start_arr = numpy.where(self.grid == 2)
        self.setStartRow=int(start_arr[0][0])
        self.setStartCol=int(start_arr[1][0])

        end_arr = numpy.where(self.grid == 3)
        self.setEndRow=int(end_arr[0][0])
        self.setEndCol=int(end_arr[1][0])

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
        if self.grid[row,column] == self.OBSTACLE:
            return neighbours
    
        nextRow = row + 1    
        if (self.isInGrid(nextRow,column) is True and self.grid[nextRow][column] != self.OBSTACLE):
            neighbours.append([nextRow,column])

        previousRow = row - 1    
        if (self.isInGrid(previousRow,column) is True and self.grid[previousRow][column] != self.OBSTACLE):
            neighbours.append([previousRow,column])

        nextColumn = column + 1    
        if (self.isInGrid(row,nextColumn) is True and self.grid[row][nextColumn] != self.OBSTACLE):
            neighbours.append([row,nextColumn])

        previousColumn = column - 1    
        if (self.isInGrid(row,previousColumn) is True and self.grid[row][previousColumn] != self.OBSTACLE):
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

    
    def generateResultPath(self,came_from):
        result_path = []

        #############################
        # Here Creation of Path starts
        #############################
        startKey = self.gridElementToString(self.setStartRow , self.setStartCol)
        currentKey = self.gridElementToString(self.setEndRow , self.setEndCol)
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
            nextPath = next.split(",")
            result_path.append([int(nextPath[0]),int(nextPath[1])])
        

        return result_path


    #############################
    # Definition of BreadthFirst algorithm
    #
    # implementation taken from https://www.redblobgames.com/pathfinding/a-star/introduction.html
    #############################
    def breadthFirst(self):
        result_path=[]
        print("Start of BreadthFirst Solver...")

        print("Start = " , self.setStartRow , self.setStartCol)
        print("End = " , self.setEndRow , self.setEndCol)
        print("Maze = \n" , self.grid)

#        print("Neighbours [0,4] : " , self.getNeighbours(0,4))

        #############################
        # Here Breadth First starts
        #############################
        start = [self.setStartRow,self.setStartCol]
        frontier = queue.Queue()
        frontier.put(start)
        startKey = self.gridElementToString(self.setStartRow , self.setStartCol)

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

        result_path = self.generateResultPath(came_from)

        print("Resulting length BreadthFirst Solution: " , len(result_path))
        print("Resulting BreadthFirst Solution Path = " , result_path)

        print("Finished BreadthFirst Solver....")

        return result_path

    #############################
    # Definition of A* algorithm
    #
    # implementation taken from https://www.redblobgames.com/pathfinding/a-star/introduction.html
    #############################
    def aStar(self):
        result_path=[]
        print("Start of A* Solver...")

        print("Start = " , self.setStartRow , self.setStartCol)
        print("End = " , self.setEndRow , self.setEndCol)
        print("Maze = \n" , self.grid)

#        print("Neighbours [0,4] : " , self.getNeighbours(0,4))

        #############################
        # Here A* starts
        #############################
        start = [self.setStartRow,self.setStartCol]
        frontier = queue.PriorityQueue()
        frontier.put((0,start))

        startKey = self.gridElementToString(self.setStartRow , self.setStartCol)
        came_from = {}
        came_from[startKey] = None

        cost_so_far = {}
        cost_so_far[startKey] = 0

        goal = [self.setEndRow , self.setEndCol]
        
        while not frontier.empty():
            current = frontier.get()[1]
            currentKey = self.gridElementToString(current[0] , current[1])
            #print("First Queue Element = " , currentKey)

            if self.isSameGridElement(current,goal):
                break

            for next in self.getNeighbours(current[0],current[1]):
                new_cost =  cost_so_far[currentKey] + 1     # + 1 is extremely important, otherwise you would not punish additional moves!!!
                                                            # + 1 = graph costs

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


        result_path = self.generateResultPath(came_from)

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
