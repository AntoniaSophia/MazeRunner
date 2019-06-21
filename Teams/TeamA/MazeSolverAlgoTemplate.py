import sys
from math import sqrt
import numpy
import queue

class MazeSolverAlgo:

    EMPTY = 0       # empty cell
    OBSTACLE = 1    # cell with obstacle / blocked cell
    START = 2       # the start position of the maze (red color)
    TARGET = 3      # the target/end position of the maze (green color)

    def __init__(self):
        # TODO: this is you job now :-)
        pass

    def setDimRows(self, rows):
        # TODO: this is you job now :-)
        pass

    def setDimCols(self, cols):
        # TODO: this is you job now :-)
        pass
        
    def setStartCol(self, col):
        # TODO: this is you job now :-)
        pass

    def setStartRow(self, row):
        # TODO: this is you job now :-)
        pass

    def setEndCol(self, col):
        # TODO: this is you job now :-)
        pass

    def setEndRow(self, row):
        # TODO: this is you job now :-)
        pass

    def setBlocked(self,row ,col):
        # TODO: this is you job now :-)
        pass

    def startMaze(self):
        # TODO: this is you job now :-)
        pass


    def startMaze(self, columns, rows):
        #populate grid with zeros
        # TODO: this is you job now :-)
        pass

    def endMaze(self):
        # TODO: this is you job now :-)
        pass

    def printMaze(self):
        # TODO: this is you job now :-)
        pass

    def loadMaze(self,pathToConfigFile):
        # check whether a function numpy.loadtxt() could be useful
        # TODO: this is you job now :-)
        pass

    def clearMaze(self):
        # TODO: this is you job now :-)
        pass
  
 
    def isInGrid(self,row,column):
        # TODO: this is you job now :-)
        pass


    # TODO: Add a Unit Test Case --> Very good example for boundary tests and condition coverage
    def getNeighbours(self,row,column):
        # TODO: this is you job now :-)
        pass

    # result should be a string row,column
    def gridElementToString(self,row,col):
        # TODO: this is you job now :-)
        pass
    
    # check whether two different grid elements are identical
    def isSameGridElement(self, aGrid, bGrid):
        # TODO: this is you job now :-)
        pass


    def heuristic(self, aGrid, bGrid):
        # TODO: this is you job now :-)
        pass

    
    def generateResultPath(self,came_from):
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



    def solveMaze(self):
        return self.myMazeSolver()

if __name__ == '__main__':
    mg = MazeSolverAlgo()
    mg.loadMaze("c:\\temp\\maze1.txt")
   
    for step in  mg.solveMaze():
        step_str = '{},{}'.format(step[0],step[1])
        #print(step_str)
