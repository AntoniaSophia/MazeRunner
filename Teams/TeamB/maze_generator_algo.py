import sys
from random import shuffle
import numpy

def shuffled(x):
    y = list(x)
    shuffle(y)
    return y

DIRECTIONS = (
    (0, -1),
    (0, 1),
    (1, 0),
    (-1, 0),
)

try:
    # Python 2
    xrange
except NameError:
    # Python 3, xrange is now named range
    xrange = range


class MazeGeneratorAlgo:

    def getMaze(self):
        return self.grid

    def __init__(self, dimensionRow, dimensionCol,complexity, density):
        """
        Constructor
        """
        self.rows = int(dimensionRow)
        self.columns = int(dimensionCol)
        self.complexity=float(complexity)/100.0
        self.density=float(density)/100.0

        self.robotStart_row = 0  # the initial position of the robot
        self.robotStart_col = 0  # the initial position of the robot        
        self.targetPos_row  = 0  # the position of the target
        self.targetPos_col  = 0  # the position of the target        

        self.grid = [[]]            # the grid
        self.shape = "Square"       # Square is initially selected

        self.array = numpy.array([0] * (self.rows * self.columns))

    def createMaze(self):
        fields = self.make_maze(self.columns, self.rows)
        
        w = (2)*self.columns+1
        h = (2)*self.rows+1
        grid = numpy.array(fields).reshape(w,h)
        self.grid = numpy.where(grid == 1, 0, 1)
        print(self.grid)

        # for y in xrange(h):
        #     print( "".join(map(lambda x: x and " " or "#", fields[y*w:y*w+w])))

    def make_maze(self, width, height, cellsize=1):
        cellsize1 = cellsize+1 # cellsize including one wall
        field_width = width*cellsize1+1
        field_height = height*cellsize1+1
        field = [0]*(field_width*field_height)
        stack = [(0, 0, shuffled(DIRECTIONS))]
        while stack:
            x, y, directions = stack[-1]
            dx, dy = directions.pop()
            # no other ways to go from here
            if not directions:
                stack.pop()
            # new cell
            nx = x+dx
            ny = y+dy
            # out of bounds
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            # index of new cell in field
            fx = 1+nx*cellsize1
            fy = 1+ny*cellsize1
            fi = fx+fy*field_width
            # already visited
            if field[fi]:
                continue
            # tear down walls
            if dx > 0:
                a = -1
                b = field_width
            elif dx < 0:
                a = cellsize
                b = field_width
            elif dy > 0:
                a = -field_width
                b = 1
            else:
                a = cellsize*field_width
                b = 1
            for offset in xrange(cellsize):
                field[fi+a+b*offset] = 1
            # clear cell
            for y in xrange(0, cellsize):
                for x in xrange(0, cellsize):
                    field[fi+x+y*field_width] = 1
            # visit cell
            stack.append([nx, ny, shuffled(DIRECTIONS)])
        return field

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("Usage: %s width height cellsize" % sys.argv[0])
    width, height, cellsize = map(int, sys.argv[1:])
    fields = make_maze(width, height, cellsize)
    w = (cellsize+1)*width+1
    h = (cellsize+1)*height+1
    for y in xrange(h):
        print( "".join(map(lambda x: x and " " or "#", fields[y*w:y*w+w])))