import queue
import numpy


class MazeSolverAlgoAStar:

    EMPTY = 0       # empty cell
    OBSTACLE = 1    # cell with obstacle
    START = 2       # the position of the robot
    TARGET = 3      # the position of the target

    def __init__(self):
        self.master = 0
        self.dimCols = 0
        self.dimRows = 0
        self.startCol = 0
        self.startRow = 0
        self.endCol = 0
        self.endRow = 0
        self.grid = [[]]
        print("[MazeSolverAlgoAStar]: Instantiating of MazeSolverAlgoAStar successful.")

    def setStartCol(self, col):
        self.startCol = col

    def setStartRow(self, row):
        self.startRow = row

    def setEndCol(self, col):
        self.endCol = col

    def setEndRow(self, row):
        self.endRow = row

    def setBlocked(self, row, col):
        self.grid[row][col] = self.OBSTACLE

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

        if self.dimCols > 0 and self.dimRows > 0:
            self.grid = numpy.empty((self.dimCols, self.dimRows), dtype=int)
            for i in range(self.dimRows):
                for j in range(self.dimCols):
                    self.grid[i][j] = 0

    def endMaze(self):
        self.grid[self.startRow][self.startCol] = self.START
        self.grid[self.endRow][self.endCol] = self.TARGET

    def printMaze(self):
        print(self.grid)

    def loadMaze(self, pathToConfigFile):
        self.grid = numpy.loadtxt(pathToConfigFile, delimiter=',', dtype=int)
        self.startMaze(self.grid.shape[0], self.grid.shape[1])
        self.grid = numpy.loadtxt(pathToConfigFile, delimiter=',', dtype=int)
        start_arr = numpy.where(self.grid == 2)
        self.startRow = int(start_arr[0][0])
        self.startCol = int(start_arr[1][0])

        end_arr = numpy.where(self.grid == 3)
        self.endRow = int(end_arr[0][0])
        self.endCol = int(end_arr[1][0])

    def clearMaze(self):
        self.startMaze()

    def isInGrid(self, row, column):
        if row < 0:
            return False

        if column < 0:
            return False

        if row >= self.grid.shape[0]:
            return False

        if column >= self.grid.shape[1]:
            return False

        return True

    def getNeighbours(self, row, column):
        neighbours = []

        # no neighbours for out-of-grid elements
        if self.isInGrid(row, column) is False:
            return neighbours

        # no neighbours for blocked grid elements
        if self.grid[row, column] == self.OBSTACLE:
            return neighbours

        nextRow = row + 1
        if (self.isInGrid(nextRow, column) is True and self.grid[nextRow][column] != self.OBSTACLE):
            neighbours.append([nextRow, column])

        previousRow = row - 1
        if (self.isInGrid(previousRow, column) is True and self.grid[previousRow][column] != self.OBSTACLE):
            neighbours.append([previousRow, column])

        nextColumn = column + 1
        if (self.isInGrid(row, nextColumn) is True and self.grid[row][nextColumn] != self.OBSTACLE):
            neighbours.append([row, nextColumn])

        previousColumn = column - 1
        if (self.isInGrid(row, previousColumn) is True and self.grid[row][previousColumn] != self.OBSTACLE):
            neighbours.append([row, previousColumn])

        return neighbours

    def gridElementToString(self, row, col):
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

    def generateResultPath(self, came_from):
        result_path = []

        #############################
        # Here Creation of Path starts
        #############################
        startKey = self.gridElementToString(self.startRow, self.startCol)
        currentKey = self.gridElementToString(self.endRow, self.endCol)
        path = []
        while currentKey != startKey:
            path.append(currentKey)
            current = came_from[currentKey]
            currentKey = self.gridElementToString(current[0], current[1])

        path.append(startKey)
        path.reverse()
        #############################
        # Here Creation of Path ends
        #############################

        for next_element in path:
            nextPath = next_element.split(",")
            result_path.append([int(nextPath[0]), int(nextPath[1])])

        return result_path

    #############################
    # Definition of A* algorithm
    #
    # implementation taken from https://www.redblobgames.com/pathfinding/a-star/introduction.html
    #############################

    def aStar(self):
        result_path = []
        print("[MazeSolverAlgoAStar]: Start of A* Solver...")

        print("[MazeSolverAlgoAStar]: Start = ", self.startRow, self.startCol)
        print("[MazeSolverAlgoAStar]: End = ", self.endRow, self.endCol)
        print("[MazeSolverAlgoAStar]: Maze = \n", self.grid)

#        print("Neighbours [0,4] : " , self.getNeighbours(0,4))

        #############################
        # Here A* starts
        #############################
        start = [self.startRow, self.startCol]
        frontier = queue.PriorityQueue()
        frontier.put((0, start))

        startKey = self.gridElementToString(self.startRow, self.startCol)
        came_from = {}
        came_from[startKey] = None

        cost_so_far = {}
        cost_so_far[startKey] = 0

        goal = [self.endRow, self.endCol]

        while not frontier.empty():
            current = frontier.get()[1]
            currentKey = self.gridElementToString(current[0], current[1])
            # print("First Queue Element = " , currentKey)

            if self.isSameGridElement(current, goal):
                break

            for next_neighbour in self.getNeighbours(current[0], current[1]):
                # + 1 is extremely important, otherwise you would not punish additional moves!!!
                new_cost = cost_so_far[currentKey] + 1
                # + 1 = graph costs

                nextKey = self.gridElementToString(next_neighbour[0], next_neighbour[1])
                if nextKey not in cost_so_far or new_cost < cost_so_far[nextKey]:
                    cost_so_far[nextKey] = new_cost
                    priority = new_cost + self.heuristic(goal, next_neighbour)
                    # print("Next = " , nextKey , " - priority = " , priority)
                    frontier.put((priority, next_neighbour))
                    came_from[nextKey] = current
        #############################
        # Here A* ends
        #############################

        result_path = self.generateResultPath(came_from)

        print("[MazeSolverAlgoAStar]: Resulting length A* Solution: ", len(result_path))
        print("[MazeSolverAlgoAStar]: Resulting A* Solution Path = ", result_path)

        print("[MazeSolverAlgoAStar]: Finished A* Solver....")

        return result_path

    def solveMaze(self):
        return self.aStar()


if __name__ == '__main__':
    mg = MazeSolverAlgoAStar()
    mg.loadMaze("..\\..\\MazeExamples\\Maze1.txt")

    for step in mg.solveMaze():
        step_str = '{},{}'.format(step[0], step[1])
        print("Go: ", step_str)
