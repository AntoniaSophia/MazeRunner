import numpy
import math


class Cell:

    def __init__(self,row=-1,col=-1):
        self.row = row
        self.column = col


    def getMoveUpCell(self, dimRows , dimColumns):
        newCell = Cell(self.row , self.column)
        if (self.row - 1 >= 0):
            newCell.moveUp()
            return newCell

        return None

    def getMoveDownCell(self, dimRows, dimColumns):
        newCell = Cell(self.row , self.column)
        if (self.row + 1 < dimRows):
            newCell.moveDown()
            return newCell

        return None

    def getMoveLeftCell(self, dimRows , dimColumns):
        newCell = Cell(self.row , self.column)
        if (self.column - 1 >= 0):
            newCell.moveLeft()
            return newCell

        return None

    def getMoveRightCell(self, dimRows , dimColumns):
        newCell = Cell(self.row , self.column)
        if (self.column + 1 < dimColumns):
            newCell.moveRight()
            return newCell

        return None

    def moveUp(self):
        self.row = self.row - 1

    def moveDown(self):
        self.row = self.row + 1

    def moveLeft(self):
        self.column = self.column - 1

    def moveRight(self):
        self.column = self.column + 1

    def equals(self, aCell):
        if (self.column == aCell.column) and (self.row == aCell.row):
            return True
        return False

    def __eq__(self, other):
        return self.equals(other)

    def distance(self, aCell):
        dX = self.column - aCell.column
        dY = self.row - aCell.row
        return (dX*dX) + (dY*dY)

    def displayCell(self):
        print("Cell: r = " , self.row , "   c = " , self.column)




class MazeSolverAlgo:
    EMPTY = 0       # empty cell
    OBST = 1        # cell with obstacle
    ROBOT = 2       # the position of the robot
    TARGET = 3      # the position of the target

    def __init__(self):
        self.robotStart_row = 0
        self.robotStart_col = 0

        self.targetPos_row = 0
        self.targetPos_col = 0

        self.dimRows = 0
        self.dimColumns = 0
        print("Initialize a Maze Solver")
        self.foundPath=[]



    def setDimRows(self, rows):
        self.dimRows = rows

    def setDimCols(self, cols):
        self.dimColumns = cols

    def setStartCol(self, col):
        self.robotStart_col = col

    def setStartRow(self, row):
        self.robotStart_row = row

    def setEndCol(self, col):
        self.targetPos_col = col

    def setEndRow(self, row):
        self.targetPos_row = row

    def setBlocked(self,row,col):
        self.grid[row][col]=1


    def startMaze(self):
        self.robotStart_row = 0
        self.robotStart_col = 0

        self.targetPos_row = 0
        self.targetPos_col = 0

        self.dimRows = 0
        self.dimColumns = 0

        self.grid=[[]]
    
    def startMaze(self, rows ,columns):
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


    def calculatePathThroughMaze(self, startCell , endCell, pathToMaze):
        if len(self.foundPath) > 1:
            return

        if startCell.equals(endCell):
            self.foundPath = pathToMaze.copy()
            return 

        getUpCell = startCell.getMoveUpCell(self.dimRows, self.dimColumns)
        getDownCell = startCell.getMoveDownCell(self.dimRows, self.dimColumns)
        getLeftCell = startCell.getMoveLeftCell(self.dimRows, self.dimColumns)
        getRightCell = startCell.getMoveRightCell(self.dimRows, self.dimColumns)

        if getUpCell is not None and self.containedAlreadyInPath(getUpCell,pathToMaze) is False:
            if self.grid[getUpCell.row][getUpCell.column] == 0 or self.grid[getUpCell.row][getUpCell.column] == 3:
                nextPath = pathToMaze.copy()
                nextPath.append(getUpCell)
                #print("Going up...")
                #self.printPath(nextPath)
                if len(self.foundPath) > 1:
                    return
                else: 
                    self.calculatePathThroughMaze(getUpCell, endCell , nextPath)

        if getDownCell is not None and self.containedAlreadyInPath(getDownCell,pathToMaze) is False:
            if self.grid[getDownCell.row][getDownCell.column] == 0 or self.grid[getDownCell.row][getDownCell.column] == 3:
                nextPath = pathToMaze.copy()
                nextPath.append(getDownCell)
                #print("Going down...")
                #self.printPath(nextPath)
                if len(self.foundPath) > 1:
                    return
                else: 
                    self.calculatePathThroughMaze(getDownCell, endCell , nextPath)

        if getLeftCell is not None  and self.containedAlreadyInPath(getLeftCell,pathToMaze) is False:
            if self.grid[getLeftCell.row][getLeftCell.column] == 0 or self.grid[getLeftCell.row][getLeftCell.column] == 3:
                nextPath = pathToMaze.copy()
                nextPath.append(getLeftCell)
                #print("Going left...")
                #self.printPath(nextPath)
                if len(self.foundPath) > 1:
                    return
                else: 
                    self.calculatePathThroughMaze(getLeftCell, endCell , nextPath)

        if getRightCell is not None  and self.containedAlreadyInPath(getRightCell,pathToMaze) is False:
            if self.grid[getRightCell.row][getRightCell.column] == 0 or self.grid[getRightCell.row][getRightCell.column] == 3:
                nextPath = pathToMaze.copy()
                nextPath.append(getRightCell)
                #print("Going right...")
                #self.printPath(nextPath)
                if len(self.foundPath) > 1:
                    return
                else: 
                    self.calculatePathThroughMaze(getRightCell, endCell , nextPath)

  
        return 


    def containedAlreadyInPath(self, aCell, aPath):
        if aCell is None or aPath is None or len(aPath) == 0:
            return False

        i = 0
        while i < len(aPath):
            if aCell.equals(aPath[i]):
                return True
            i += 1
        
        return False

    def printPath(self, aPath):
        if aPath is None or len(aPath) == 0:
            print("No path to display...")
            return

        i = 0
        while i < len(aPath):
            print(i , ". Step: (" , aPath[i].row , "),(" , aPath[i].column, ")")
            i += 1
        

    def solveMaze(self):
        print("*************Solve Maze*****************")
        self.printMaze()
        startCell = Cell(self.robotStart_row , self.robotStart_col)
        endCell = Cell(self.targetPos_row , self.targetPos_col)

        pathToMaze = []
        self.calculatePathThroughMaze(startCell, endCell , pathToMaze)
        print("Final Result!")
        self.printPath(self.foundPath)
        print("End Final Result!")

        res = []
        i = 0
        while i < len(self.foundPath):        
            temp = [self.foundPath[i].row , self.foundPath[i].column]
            res.append(temp)
            i+=1

        return res
        #return [(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(3,2),(3,3),(3,4),(4,4)]



