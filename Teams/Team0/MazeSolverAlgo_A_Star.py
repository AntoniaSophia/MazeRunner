import sys
from math import sqrt
import numpy
class Tile:

    def __init__(self, char, x, y):
        self.char = char
        self.g = 0
        self.h = 0
        self.x = x
        self.y = y
        self.parent = None
        self.setReachable()

    def setReachable(self):
        self.reachable = True
        if self.char == 1:
            self.reachable = False

    def move_cost(self, other):
        if other.reachable:
            return 10
        else:
            return 1000

class AStar:

    def __init__(self, maze):
        self.maze = maze

    def getAdjacent(self, cell):
        mazeWidth = len(self.maze[0])
        mazeHeight = len(self.maze)
        ret = []
        if cell.y > 0:
            ret.append(self.getTileAtCoords(cell.x, cell.y - 1))
        if cell.x < mazeWidth - 1:
            ret.append(self.getTileAtCoords(cell.x + 1, cell.y))
        if cell.y < mazeHeight - 1:
            ret.append(self.getTileAtCoords(cell.x, cell.y + 1))
        if cell.x > 0:
            ret.append(self.getTileAtCoords(cell.x - 1, cell.y))
        return ret

    def heuristic(self, cell):
        return sqrt((self.end.x - cell.x)**2 + (self.end.y - cell.y)**2)

    def constructPath(self, current):
        path = []
        while current.parent:
            path.append(current)
            current = current.parent
        path.append(current)
        return path[::-1]

    def getTileAtCoords(self, x, y):
        try:
            return self.maze[y][x]
        except KeyError as e:
            print ("Could not find tile at position x: {} y: {}".format(x, y))

    def search(self, current, end):
        self.end = end
        openset = set()
        closedset = set()
        openset.add(current)
        while len(openset):
            current = min(openset, key=lambda o:o.g + o.h)
            if current == end:
                return self.constructPath(current)
            openset.remove(current)
            closedset.add(current)
            for node in self.getAdjacent(current):
                if node in closedset:
                    continue
                if node in openset:
                    new_g = current.g + current.move_cost(node)
                    if node.g > new_g:
                        node.g = new_g
                        node.parent = current
                else:
                    node.g = current.g + current.move_cost(node)
                    node.h = self.heuristic(node)
                    node.parent = current
                    openset.add(node)

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

    def loadMaze(self,pathToConfigFile):
        self.grid=numpy.loadtxt(pathToConfigFile, delimiter=',',dtype=int)
        self.setDimCols=self.grid.shape[0]
        self.setDimRows=self.grid.shape[1]
        start_arr = numpy.where(self.grid == 2)
        self.setStartCols=int(start_arr[0][0])
        self.setStartRows=int(start_arr[1][0])
        end_arr = numpy.where(self.grid == 3)
        self.setEndCols=int(end_arr[0][0])
        self.setEndRows=int(end_arr[1][0])

        print(self.setStartCols,"#",self.setStartRows)
        print(self.setEndCols,"#",self.setEndRows)
    
    def convertGrid(self):
        maze = []
        row_pos=0
        for row in self.grid:
            col_pos=0
            row_tile = []
            for col in row:
                row_tile.append(Tile(col, col_pos, row_pos))
                col_pos+=1
            maze.append(row_tile)
            row_pos+=1
        return maze

    def solveMaze(self):
        print("aStar Solver")
        result_path=[]
        aStar = AStar(self.convertGrid())
        print("Grid converted for a Star")
        for tile in aStar.search(aStar.maze[self.robotStart_row][self.robotStart_row], aStar.maze[self.targetPos_col][self.targetPos_row]):
            step=[tile.y,tile.x]
            result_path.append(step)
        print("aStar Finished")
        return result_path

if __name__ == '__main__':
    mg = MazeSolverAlgo()
    mg.loadMaze("c:\\temp\\maze.txt")
   
    for step in  mg.solveMaze():
        step_str = '{},{}'.format(step[0],step[1])
        print(step_str)
