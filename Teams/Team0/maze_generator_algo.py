from tkinter import *
from tkinter import font
from tkinter import messagebox
from functools import partial
from operator import attrgetter
from random import shuffle, randrange
import webbrowser
import numpy
import math
import os
import paho.mqtt.client as mqtt

class MazeGeneratorAlgo:
    class Cell(object):
        """
        Helper class that represents the cell of the grid
        """

        def __init__(self, row, col):
            self.row = row  # the row number of the cell(row 0 is the top)
            self.col = col  # the column number of the cell (column 0 is the left)
            self.prev = self.__class__

        def __eq__(self, other):
            """
            useful Cell equivalence
            """
            if isinstance(other, self.__class__):
                return self.row == other.row and self.col == other.col
            else:
                return False

    INFINITY = sys.maxsize  # The representation of the infinite
    EMPTY = 0       # empty cell
    OBST = 1        # cell with obstacle
    ROBOT = 2       # the position of the robot
    TARGET = 3      # the position of the target
    FRONTIER = 4    # cells that form the frontier (OPEN SET)
    CLOSED = 5      # cells that form the CLOSED SET
    ROUTE = 6       # cells that form the robot-to-target path

    MSG_DRAW_AND_SELECT = "Das ist ein Text der von außen gesteuert werden kann"
    MSG_SELECT_STEP_BY_STEP_ETC = "Click 'Step-by-Step' or 'Animation' or 'Clear'"
    MSG_NO_SOLUTION = "There is no path to the target !!!"

    def getMaze(self):
        return self.grid

    def __init__(self, dimensionRow, dimensionCol,startCol,startRow,endCol,endRow):
        """
        Constructor
        """
        self.rows = dimensionRow
        self.columns = dimensionCol
        self.square_size = 0        # the cell size in pixels
        self.arrow_size = 0         # the size of the tips of the arrow pointing the predecessor cell

        self.radius = 0.0           # the radius of triangular and hexagonal cells
        self.height = 0.0           # half the height of hexagonal cells or the height of triangular cells
        self.edge = 0.0             # the edge of the triangular cell

        self.openSet = []           # the OPEN SET
        self.closedSet = []         # the CLOSED SET
        self.graph = []             # the set of vertices of the graph to be explored by Dijkstra's algorithm

        self.robotStart = self.Cell(startRow, startCol)    # the initial position of the robot
        self.targetPos = self.Cell(endRow,endCol)  # the position of the target

        self.grid = [[]]            # the grid
        self.dist = self.INFINITY   # distance of the point the user clicked on the canvas from the centre of some cell
        self.realTime = False       # Solution is displayed instantly
        self.found = False          # flag that the goal was found
        self.searching = False      # flag that the search is in progress
        self.endOfSearch = False    # flag that the search came to an end
        self.animation = False      # flag that the animation is running
        self.delay = 500            # time delay of animation (in msec)
        self.expanded = 0           # the number of nodes that have been expanded
        self.shape = "Square"       # Square is initially selected

        self.array = numpy.array([0] * (dimensionRow * dimensionCol))
        self.cur_row = self.cur_col = self.cur_val = 0
        memo_colors = ("RED", "GREEN", "BLUE", "CYAN")

    @staticmethod
    def make_maze(w, h):
        """
        Creates a random, perfect (without cycles) maze
        From http://rosettacode.org/wiki/Maze_generation

        recursive backtracking algorithm

        :param w:   the width of the maze
        :param h:   the height of the maze

        :return:    the maze as a string
        """
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [["| "] * w + ['|'] for _ in range(h)] + [[]]
        hor = [["+-"] * w + ['+'] for _ in range(h + 1)]

        def walk(x, y):
            vis[y][x] = 1

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]:
                    continue
                if xx == x:
                    hor[max(y, yy)][x] = "+ "
                if yy == y:
                    ver[y][max(x, xx)] = "  "
                walk(xx, yy)

        walk(randrange(w), randrange(h))

        s = ""
        for (a, b) in zip(hor, ver):
            s += ''.join(a + b)
        return s

    def initialize_grid(self, make_maze):
        """
        Creates a new clean grid or a new maze

        :param make_maze: flag that indicates the creation of a random maze
        """
        # the square maze must have an odd number of rows
        # the rows of the triangular maze must be at least 8 and a multiple of 4
        if make_maze and (self.rows % 2 != 1 if self.shape == "Square" else self.rows % 4 !=0):
            if self.shape == "Square":
                self.rows -= 1
            else:
                self.rows = max(int(self.rows/4)*4,8)
            
        # a hexagonal grid must have an odd number of columns
        if self.shape == "Hexagon" and self.columns % 2 != 1:
            self.columns -= 1
            
        # the columns of the triangular maze must be rows+1
        if make_maze and self.shape == "Triangle":
            self.columns = self.rows + 1
            
        # the columns of the square maze must be equal to rows
        if make_maze and self.shape == "Square":
            self.columns = self.rows
            
        self.grid = self.array[:self.rows*self.columns]
        self.grid = self.grid.reshape(self.rows, self.columns)

        # Calculation of the edge and the height of the triangular cell
        if self.shape == "Triangle":
            self.edge = min(500 / (int(self.columns/2) + 1), 1000 / (self.rows * math.sqrt(3)))
            self.height = self.edge * math.sqrt(3) / 2
            self.radius = self.height*2/3
            self.arrow_size = int(self.edge / 4)

        # Calculation of the size of the square cell
        if self.shape == "Square":
            self.square_size = int(500 / (self.rows if self.rows > self.columns else self.columns))
            self.arrow_size = int(self.square_size / 2)

        # Calculation of the radius and the half height of the hexagonal cell
        if self.shape == "Hexagon":
            self.radius = min(1000 / (3 * self.columns + 1), 500 / (self.rows * math.sqrt(3)))
            self.height = self.radius * math.sqrt(3) / 2
            self.arrow_size = int(self.radius / 2)

        # # Creation of the canvas' background
        # if self.shape == "Triangle":
        #     self.canvas.configure(width=(self.columns/2 + 0.5) * self.edge + 1, height=self.rows * self.height + 1)
        #     self.canvas.place(x=10, y=10)
        #     self.canvas.create_rectangle(0, 0, (self.columns/2 + 0.5) * self.edge + 1,
        #                                  self.rows * self.height + 1, width=0, fill="DARK GREY")
        # if self.shape == "Square":
        #     self.canvas.configure(width=self.columns * self.square_size + 1, height=self.rows * self.square_size + 1)
        #     self.canvas.place(x=10, y=10)
        #     self.canvas.create_rectangle(0, 0, self.columns*self.square_size+1,
        #                                  self.rows*self.square_size+1, width=0, fill="DARK GREY")
        # if self.shape == "Hexagon":
        #     self.canvas.configure(width=(self.columns-1)/2*3*self.radius + 2*self.radius,
        #                           height=self.rows*2*self.height + 1)
        #     self.canvas.place(x=10, y=10)
        #     self.canvas.create_rectangle(0, 0, (self.columns-1)/2*3*self.radius + 2*self.radius,
        #                                  self.rows*2*self.height + 1, width=0, fill="DARK GREY")

        for r in range(self.rows):
            for c in list(range(self.columns)):
                self.grid[r][c] = self.EMPTY
        if self.shape == "Square":
            self.robotStart = self.Cell(self.rows-2, 1)
            self.targetPos = self.Cell(1, self.columns-2)
        else:
            self.robotStart = self.Cell(self.rows-1, 0)
            self.targetPos = self.Cell(0, self.columns-1)

        
        if make_maze:
            if self.shape == "Square":
                maze = self.make_maze(int(self.rows / 2), int(self.columns / 2))
                for r in range(self.rows):
                    for c in range(self.columns):
                        if maze[r * self.columns + c : r * self.columns + c + 1] in "|-+":
                            self.grid[r][c] = self.OBST
            else:
                maze = self.make_maze(int(self.rows / 4), int(self.columns / 4))
                rows2 = int(self.rows / 2) + 1
                cols2 = int(self.columns / 2) + 1
                for r1 in range(rows2):
                    for c1 in range(cols2):
                        if maze[r1 * cols2 + c1 : r1 * cols2 + c1 + 1] in "|-+":
                            if rows2-2+r1-c1 >= 0:
                                self.grid[rows2-2+r1-c1][r1+c1] = self.OBST
                            if rows2 - 1 + r1 - c1 < self.rows:
                                self.grid[rows2 - 1 + r1 - c1][r1 + c1] = self.OBST
                self.grid[self.robotStart.row][self.robotStart.col] = self.EMPTY
                self.grid[self.targetPos.row][self.targetPos.col] = self.EMPTY
                self.robotStart.row = self.rows-2
                self.robotStart.col = int(self.columns/2)
                self.targetPos.row = 1
                self.targetPos.col = int(self.columns/2)
                self.grid[self.robotStart.row][self.robotStart.col] = self.ROBOT
                self.grid[self.targetPos.row][self.targetPos.col] = self.TARGET
        if self.shape == "Hexagon":
            for c in range(self.columns):
                if c % 2 != 0:
                    self.grid[self.rows-1][c] = self.OBST


if __name__ == '__main__':
    mg = MazeGeneratorAlgo()
    mg.initialize_grid(True)
    mg.printMaze()
