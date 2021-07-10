import os
import sys
import getopt
import time
import numpy
import paho.mqtt.client as mqtt
import collections
import random
import numpy as np
import enum


class MazeError(Exception):
    """Maze error class."""


def stack_empty():
    """Creates empty spaghetti stack."""
    return ()


def stack_push(stack, item):
    """Pushes item into spaghetti stack."""
    return item, stack


def stack_deque(stack):
    """Converts spaghetti stack into deque."""
    deque = collections.deque()
    while stack:
        item, stack = stack
        deque.appendleft(item)

    return deque


def color(offset, iteration):
    """Returns color for current iteration."""
    clr = iteration * offset

    return clr, 0, 255 - clr


def draw_path(solution, stack):
    """Draws path in solution."""
    total = 2 * len(stack)
    offset = 255 / total
    iteration = 2

    x1, y1 = stack.popleft()
    solution[x1, y1] = color(offset, 0)
    while iteration < total:
        x2, y2 = stack.popleft()
        solution[x2, y2] = color(offset, iteration)
        solution[(x1 + x2) // 2, (y1 + y2) // 2] = color(offset, iteration - 1)
        x1, y1 = x2, y2
        iteration += 2


def upscale(maze, scale):
    """Upscales maze."""
    if not isinstance(maze, np.ndarray):
        maze = np.array(maze)
    if scale <= 1:
        return maze

    return maze.repeat(scale, axis=0).repeat(scale, axis=1)


def get_scale(maze):
    """Calculates scale of upscaled maze."""
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x, y, 0] != 0:
                return x


def downscale(maze):
    """Downscales maze."""
    if not isinstance(maze, np.ndarray):
        maze = np.array(maze)
    scale = get_scale(maze)
    if scale <= 1:
        return maze

    return maze[::scale, ::scale]


class MazeBase(object):
    """This class contains base functions."""
    class Create(enum.Enum):
        """Enum for creation algorithms."""
        BACKTRACKING = "Recursive backtracking algorithm"
        HUNT = "Hunt and kill algorithm"
        ELLER = "Eller's algorithm"
        SIDEWINDER = "Sidewinder algorithm"
        PRIM = "Prim's algorithm"
        KRUSKAL = "Kruskal's algorithm"

    def __init__(self):
        """Constructor."""
        self.maze = None
        self.solution = None
        self._dll = None

    @property
    def row_count_with_walls(self):
        """Returns the mazes row count with walls."""
        return self.maze.shape[0]

    @property
    def col_count_with_walls(self):
        """Returns the mazes column count with walls."""
        return self.maze.shape[1]

    @property
    def row_count(self):
        """Returns the mazes row count."""
        return self.row_count_with_walls // 2

    @property
    def col_count(self):
        """Returns the mazes column count."""
        return self.col_count_with_walls // 2


class Maze(MazeBase):
    # pylint: disable=no-member
    EMPTY = 0       # empty cell
    OBST = 1        # cell with obstacle
    ROBOT = 2       # the position of the robot
    TARGET = 3      # the position of the target

    """This class contains the relevant algorithms for creating and solving."""

    def __init__(self):
        """Constructor."""
        super(Maze, self).__init__()

        self._dir_one = [
            lambda x, y: (x + 1, y),
            lambda x, y: (x - 1, y),
            lambda x, y: (x, y - 1),
            lambda x, y: (x, y + 1)
        ]
        self._dir_two = [
            lambda x, y: (x + 2, y),
            lambda x, y: (x - 2, y),
            lambda x, y: (x, y - 2),
            lambda x, y: (x, y + 2)
        ]
        self._range = list(range(4))

    def create(self, row_count, col_count, algorithm):
        """Creates a maze for a given row and column count."""
        if (row_count or col_count) <= 0:
            raise utils.MazeError("Row or column count cannot be smaller than zero.")

        self.maze = np.zeros((2 * row_count + 1, 2 * col_count + 1), dtype=np.uint8)

        if algorithm == Maze.Create.BACKTRACKING:
            return self._recursive_backtracking()
        if algorithm == Maze.Create.HUNT:
            return self._hunt_and_kill()
        if algorithm == Maze.Create.ELLER:
            return self._eller()
        if algorithm == Maze.Create.SIDEWINDER:
            return self._sidewinder()
        if algorithm == Maze.Create.PRIM:
            return self._prim()
        if algorithm == Maze.Create.KRUSKAL:
            return self._kruskal()

        raise utils.MazeError(
            "Wrong algorithm <{}>.\n"
            "Use \"Maze.Create.<algorithm>\" to choose an algorithm.".format(algorithm)
        )

    @property
    def _random(self):
        """Returns a random range to iterate over."""
        random.shuffle(self._range)
        return self._range

    def _out_of_bounds(self, x, y):
        """Checks if indices are out of bounds."""
        return x < 0 or y < 0 or x >= self.row_count_with_walls or y >= self.col_count_with_walls

    def _create_walk(self, x, y):
        """Randomly walks from one pointer within the maze to another one."""
        for idx in self._random:  # Check adjacent cells randomly
            tx, ty = self._dir_two[idx](x, y)
            if not self._out_of_bounds(tx, ty) and self.maze[tx, ty] == 0:  # Check if unvisited
                self.maze[tx, ty] = self.maze[self._dir_one[idx](x, y)] = 1  # Mark as visited
                return tx, ty  # Return new cell

        return None, None  # Return stop values

    def _create_backtrack(self, stack):
        """Backtracks the stack until walking is possible again."""
        while stack:
            x, y = stack.pop()
            for direction in self._dir_two:  # Check adjacent cells
                tx, ty = direction(x, y)
                if not self._out_of_bounds(tx, ty) and self.maze[tx, ty] == 0:  # Check if unvisited
                    return x, y  # Return cell with unvisited neighbour

        return None, None  # Return stop values if stack is empty

    def _recursive_backtracking(self):
        """Creates a maze using the recursive backtracking algorithm."""
        stack = collections.deque()  # List of visited cells [(x, y), ...]

        x = 2 * random.randint(0, self.row_count - 1) + 1
        y = 2 * random.randint(0, self.col_count - 1) + 1
        self.maze[x, y] = 1  # Mark as visited

        while x and y:
            while x and y:
                stack.append((x, y))
                x, y = self._create_walk(x, y)
            x, y = self._create_backtrack(stack)

    def _hunt(self, hunt_list):
        """Scans the maze for new position."""
        while hunt_list:
            for x in hunt_list:
                finished = True
                for y in range(1, self.col_count_with_walls - 1, 2):
                    if self.maze[x, y] == 0:  # Check if unvisited
                        finished = False
                        for direction in self._dir_two:  # Check adjacent cells
                            tx, ty = direction(x, y)
                            if not self._out_of_bounds(tx, ty) and self.maze[tx, ty] == 0:  # Check if visited
                                return x, y  # Return visited neighbour of unvisited cell
                if finished:
                    hunt_list.remove(x)  # Remove finished row
                    break  # Restart loop

        return None, None  # Return stop values if all rows are finished

    def _hunt_and_kill(self):
        """Creates a maze using the hunt and kill algorithm."""
        hunt_list = list(range(1, self.row_count_with_walls - 1, 2))  # List of unfinished rows [x, ...]

        x = 2 * random.randint(0, self.row_count - 1) + 1
        y = 2 * random.randint(0, self.col_count - 1) + 1
        self.maze[x, y] = 1  # Mark as visited

        while hunt_list:
            while x and y:
                x, y = self._create_walk(x, y)
            x, y = self._hunt(hunt_list)

    def _eller(self):
        """Creates a maze using Eller's algorithm."""
        self.row_stack = [0] * self.col_count  # List of set indices [set index, ...]
        self.set_list = []  # List of set indices with positions [(set index, position), ...]
        self.set_index = 1

        for x in range(1, self.row_count_with_walls - 1, 2):
            connect_list = collections.deque()  # List of connections between cells [True, ...]

            # Create row stack
            if self.row_stack[0] == 0:  # Define first cell in row
                self.row_stack[0] = self.set_index
                self.set_index += 1

            for y in range(1, self.col_count):  # Define other cells in row
                if random.getrandbits(1):  # Connect cell with previous cell
                    if self.row_stack[y] != 0:  # Cell has a set
                        old_index = self.row_stack[y]
                        new_index = self.row_stack[y - 1]
                        if old_index != new_index:  # Combine both sets
                            self.row_stack = \
                                [new_index if y == old_index else y for y in self.row_stack]  # Replace old indices
                            connect_list.append(True)
                        else:
                            connect_list.append(False)
                    else:  # Cell has no set
                        self.row_stack[y] = self.row_stack[y - 1]
                        connect_list.append(True)
                else:  # Do not connect cell with previous cell
                    if self.row_stack[y] == 0:
                        self.row_stack[y] = self.set_index
                        self.set_index += 1
                    connect_list.append(False)

            # Create set list and fill cells
            for y in range(self.col_count):
                maze_col = 2 * y + 1
                self.set_list.append((self.row_stack[y], maze_col))

                self.maze[x, maze_col] = 1  # Mark as visited
                if y < self.col_count - 1:
                    if connect_list.popleft():
                        self.maze[x, maze_col + 1] = 1  # Mark as visited

            if x == self.row_count_with_walls - 2:  # Connect all different sets in last row
                for y in range(1, self.col_count):
                    new_index = self.row_stack[y - 1]
                    old_index = self.row_stack[y]
                    if new_index != old_index:
                        self.row_stack = [new_index if y == old_index else y for y in self.row_stack]  # Replace old indices
                        self.maze[x, 2 * y] = 1  # Mark as visited
                break  # End loop with last row

            self._eller_final(x)

    def _eller_final(self, x):
        # Reset row stack
        self.row_stack = [0] * self.col_count

        # Create vertical links
        self.set_list.sort(reverse=True)
        while self.set_list:
            # List of set indices with positions for one set index [(set index, position), ...]
            sub_set_list = collections.deque()
            sub_set_index = self.set_list[-1][0]
            while self.set_list and self.set_list[-1][0] == sub_set_index:  # Create sub list for one set index
                sub_set_list.append(self.set_list.pop())
            linked = False
            while not linked:  # Create at least one link for each set index
                for sub_set_item in sub_set_list:
                    if random.getrandbits(1):  # Create link
                        linked = True
                        link_set, link_position = sub_set_item

                        self.row_stack[link_position // 2] = link_set  # Assign links to new row stack
                        self.maze[x + 1, link_position] = 1  # Mark link as visited

    def _sidewinder(self):
        """Creates a maze using the sidewinder algorithm."""
        # Create first row
        for y in range(1, self.col_count_with_walls - 1):
            self.maze[1, y] = 1

        # Create other rows
        for x in range(3, self.row_count_with_walls, 2):
            row_stack = []  # List of cells without vertical link [y, ...]
            for y in range(1, self.col_count_with_walls - 2, 2):
                self.maze[x, y] = 1  # Mark as visited
                row_stack.append(y)

                if random.getrandbits(1):  # Create vertical link
                    idx = random.randint(0, len(row_stack) - 1)
                    self.maze[x - 1, row_stack[idx]] = 1  # Mark as visited
                    row_stack = []  # Reset row stack
                else:  # Create horizontal link
                    self.maze[x, y + 1] = 1  # Mark as visited

            # Create vertical link if last cell
            y = self.col_count_with_walls - 2
            self.maze[x, y] = 1  # Mark as visited
            row_stack.append(y)
            idx = random.randint(0, len(row_stack) - 1)
            self.maze[x - 1, row_stack[idx]] = 1  # Mark as visited

    def _prim(self):
        """Creates a maze using Prim's algorithm."""
        frontier = []  # List of unvisited cells [(x, y),...]

        # Start with random cell
        x = 2 * random.randint(0, self.row_count - 1) + 1
        y = 2 * random.randint(0, self.col_count - 1) + 1
        self.maze[x, y] = 1  # Mark as visited

        # Add cells to frontier for random cell
        for direction in self._dir_two:
            tx, ty = direction(x, y)
            if not self._out_of_bounds(tx, ty):
                frontier.append((tx, ty))
                self.maze[tx, ty, 0] = 1  # Mark as part of frontier

        # Add and connect cells until frontier is empty
        while frontier:
            x, y = frontier.pop(random.randint(0, len(frontier) - 1))

            # Connect cells
            for idx in self._random:
                tx, ty = self._dir_two[idx](x, y)
                if not self._out_of_bounds(tx, ty) and self.maze[tx, ty, 0] == 255:  # Check if visited
                    self.maze[x, y] = self.maze[self._dir_one[idx](x, y)] = 1  # Connect cells
                    break

            # Add cells to frontier
            for direction in self._dir_two:
                tx, ty = direction(x, y)
                if not self._out_of_bounds(tx, ty) and self.maze[tx, ty, 0] == 0:  # Check if unvisited
                    frontier.append((tx, ty))
                    self.maze[tx, ty, 0] = 1  # Mark as part of frontier

    def _kruskal(self):
        """Creates a maze using Kruskal's algorithm."""
        xy_to_set = np.zeros((self.row_count_with_walls, self.col_count_with_walls), dtype=np.uint32)
        set_to_xy = []  # List of sets in order, set 0 at index 0 [[(x, y),...], ...]
        edges = collections.deque()  # List of possible edges [(x, y, direction), ...]
        set_index = 0

        for x in range(1, self.row_count_with_walls - 1, 2):
            for y in range(1, self.col_count_with_walls - 1, 2):
                # Assign sets
                xy_to_set[x, y] = set_index
                set_to_xy.append([(x, y)])
                set_index += 1

                # Create edges
                if not self._out_of_bounds(x + 2, y):
                    edges.append((x + 1, y, "v"))  # Vertical edge
                if not self._out_of_bounds(x, y + 2):
                    edges.append((x, y + 1, "h"))  # Horizontal edge

        random.shuffle(edges)  # Shuffle to pop random edges
        while edges:
            x, y, direction = edges.pop()

            x1, x2 = (x - 1, x + 1) if direction == "v" else (x, x)
            y1, y2 = (y - 1, y + 1) if direction == "h" else (y, y)

            if xy_to_set[x1, y1] != xy_to_set[x2, y2]:  # Check if cells are in different sets
                self.maze[x, y] = self.maze[x1, y1] = self.maze[x2, y2] = 1  # Mark as visited

                new_set = xy_to_set[x1, y1]
                old_set = xy_to_set[x2, y2]

                # Extend new set with old set
                set_to_xy[new_set].extend(set_to_xy[old_set])

                # Correct sets in xy sets
                for pos in set_to_xy[old_set]:
                    xy_to_set[pos] = new_set

    def _depth_first_search_c(self, start, end):
        """Solves a maze using depth-first search in C."""
        start = start[0] * self.col_count_with_walls + start[1]
        end = end[0] * self.col_count_with_walls + end[1]

        self.solution = self.solution.flatten()
        self.get_dll().depth_first_search(
            self.maze[:, :, ::3].flatten(), self.solution, self.col_count, start, end
        )
        self.solution = self.solution.reshape((self.row_count_with_walls, self.col_count_with_walls, 3))

    def _solve_walk(self, x, y, visited):
        """Walks over a maze."""
        for idx in range(4):  # Check adjacent cells
            bx, by = self._dir_one[idx](x, y)
            if visited[bx, by, 0] == 255:  # Check if unvisited
                tx, ty = self._dir_two[idx](x, y)
                visited[bx, by, 0] = visited[tx, ty, 0] = 0  # Mark as visited
                return tx, ty  # Return new cell

        return None, None  # Return stop values

    def _solve_backtrack(self, stack, visited):
        """Backtracks a stacks."""
        while stack:
            x, y = stack.pop()
            for direction in self._dir_one:  # Check adjacent cells
                tx, ty = direction(x, y)
                if visited[tx, ty, 0] == 255:  # Check if unvisited
                    return x, y  # Return cell with unvisited neighbour

        return None, None  # Return stop values if stack is empty and no new cell was found

    def _depth_first_search(self, start, end):
        """Solves a maze using depth-first search."""
        visited = self.maze.copy()  # List of visited cells, value of visited cell is 0
        stack = collections.deque()  # List of visited cells [(x, y), ...]

        x, y = start
        visited[x, y, 0] = 0  # Mark as visited

        while x and y:
            while x and y:
                stack.append((x, y))
                if (x, y) == end:  # Stop if end has been found
                    return utils.draw_path(self.solution, stack)
                x, y = self._solve_walk(x, y, visited)
            x, y = self._solve_backtrack(stack, visited)

        raise utils.MazeError("No solution found.")

    def _enqueue(self, queue, visited):
        """Queues next cells."""
        cell = queue.popleft()
        x, y = cell[0]
        for idx in range(4):  # Check adjacent cells
            bx, by = self._dir_one[idx](x, y)
            if visited[bx, by, 0] == 255:  # Check if unvisited
                tx, ty = self._dir_two[idx](x, y)
                visited[bx, by, 0] = visited[tx, ty, 0] = 0  # Mark as visited
                queue.append(utils.stack_push(cell, (tx, ty)))

    def _breadth_first_search(self, start, end):
        """Solves a maze using breadth-first search."""
        visited = self.maze.copy()  # List of visited cells, value of visited cell is 0
        queue = collections.deque()  # List of cells [cell, ...]
        cell = utils.stack_empty()  # Tuple of current cell with according stack ((x, y), stack)

        x, y = start
        cell = utils.stack_push(cell, (x, y))
        queue.append(cell)
        visited[x, y, 0] = 0  # Mark as visited

        while queue:
            self._enqueue(queue, visited)
            if queue[0][0] == end:  # Stop if end has been found
                cell = utils.stack_push(queue[0], end)  # Push end into cell
                return utils.draw_path(self.solution, utils.stack_deque(cell))

        raise utils.MazeError("No solution found.")

    def getMaze(self):
        b= np.array(self.maze, dtype=np.int8)

        b=np.where(b==1, 9, b) 
        b=np.where(b==0, 1, b) 
        b=np.where(b==9, 0, b) 
        b[1][1]=2
        dim=b.shape
        b[dim[0]-2][dim[1]-2]=3

        return b



if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    mqtt_server = os.environ['MQTTSERVER']
else:
    mqtt_server = "127.0.0.1"


class MazeGeneratorClient:

    def onConnect(self, master, obj, flags, rc):
        # do anything if required
        # print("test_mqtt_publisher connected to mqtt-broker")
        pass

    def publish(self, topic, message=None, qos=0, retain=False):
        self.master.publish(topic, message, qos, retain)
        print("[MazeGenerator] Published message: ", topic, " --> ", message)

    def __init__(self):
        self.startCol = 2
        self.startRow = 2
        self.endCol = 7
        self.endRow = 7
        self.dimensionRow = 27
        self.dimensionCol = 27
        # self.master = mqtt.Client()
        # self.master.on_connect = self.onConnect
        # self.master.connect(mqtt_server, 1883, 60)
        print("\n[MazeGenerator] Constructor MazeGenerator successfull executed.")

    def printMaze(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                print(self.maze[i][j], end='')
            print()
        print()

    def sendMaze(self):
        self.publish("/maze", "clear")
        self.publish("/maze", "start")
        self.publish("/maze/dimCol", self.dimensionCol)
        self.publish("/maze/dimRow", self.dimensionRow)
        self.publish("/maze/startCol", self.startCol)
        self.publish("/maze/startRow", self.startRow)
        self.publish("/maze/endCol", self.endCol)
        self.publish("/maze/endRow", self.endRow)

        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if (self.maze[i][j] == 1):
                    blocked = ""
                    blocked += str(i)
                    blocked += ","
                    blocked += str(j)
                    self.publish("/maze/blocked", blocked)

                    if mqtt_server != "127.0.0.1":
                        time.sleep(0.05)
                else:
                    # do nothing because this field is not blocked
                    pass

        self.publish("/maze", "end")

        # pass

    def loadMaze(self, pathToConfigFile):
        print("[MazeGenerator] Loading maze from file", pathToConfigFile)
        self.maze = numpy.loadtxt(pathToConfigFile, delimiter=',', dtype=int)
        self.dimensionCol = self.maze.shape[0]
        self.dimensionRow = self.maze.shape[1]
        start_arr = numpy.where(self.maze == 2)
        self.startRow = int(start_arr[0][0])
        self.startCol = int(start_arr[1][0])
        end_arr = numpy.where(self.maze == 3)
        self.endRow = int(end_arr[0][0])
        self.endCol = int(end_arr[1][0])

    def saveMaze(self, pathToConfigFile):
        numpy.savetxt(pathToConfigFile, self.mga.getMaze(), fmt="%d", delimiter=",", newline="\n")

    def createNewMaze(self, width, height, complexity, density, stralgo):
        if stralgo == "backtracking":
            algorithm = Maze.Create.BACKTRACKING
        elif stralgo == "hunt":
            algorithm = Maze.Create.HUNT
        elif stralgo == "eller":
            algorithm = Maze.Create.ELLER
        elif stralgo == "sidewinder":
            algorithm = Maze.Create.SIDEWINDER
        elif stralgo == "prim":
            algorithm = Maze.Create.PRIM
        elif stralgo == "kruskal":
            algorithm = Maze.Create.KRUSKAL
        else:
            algorithm = Maze.Create.BACKTRACKING

        print("\n[MazeGenerator] Generating Maze ", width, height, complexity, density, stralgo)
        self.mga = Maze()
        self.mga.create(int(int(width)/2), int(int(height)/2), algorithm)
        self.maze = self.mga.getMaze()
        (x, y) = self.maze.shape
        self.startCol = 1
        self.startRow = 1
        self.endCol = x-2
        self.endRow = y-2
        self.maze[self.startCol, self.startRow] = Maze.ROBOT
        self.maze[self.endCol, self.endRow] = Maze.TARGET
        self.dimensionCol = x
        self.dimensionRow = y


def main(argv):
    inputfile = ''
    outputfile = ''
    width = 7
    height = 7
    complexity = 50
    density = 50
    algorithm = "backtracking"

    try:
        opts, args = getopt.getopt(argv, "ha:i:o:w:h:c:d:",
                                   ["algo=", "ifile=", "ofile=", "width=", "height=", "complexity=", "density="])
    except getopt.GetoptError:
        print('MazeGeneratorClient.py -i <inputfile> -o <outputfile> -w <width> -h <height> -c <complexity> -d <density>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('MazeGeneratorClient.py -a ' +
                  'backtracking|hunt|eller|sidewinder|prim|kruskal -i ' +
                  '<inputfile> -o <outputfile> -w <width> -h <height> -c ' +
                  '<complexity> -d <density>')
            sys.exit()
        elif opt in ("-a", "--algo"):
            algorithm = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-w", "--width"):
            width = arg
        elif opt in ("-h", "--height"):
            height = arg
        elif opt in ("-c", "--complexity"):
            complexity = arg
        elif opt in ("-d", "--density"):
            density = arg
    mg = MazeGeneratorClient()

    if len(inputfile) > 0:
        print('\n[MazeGenerator] Input maze file is: ', inputfile)
        mg.loadMaze(inputfile)
    else:
        mg.createNewMaze(width, height, complexity, density, algorithm)
        if len(outputfile) > 0:
            print('\n[MazeGenerator] Output maze file is: ', outputfile)
            mg.saveMaze(outputfile)
        else:
            print("[MazeGenerator] Sending following Maze:")
            mg.printMaze()
            mg.sendMaze()


if __name__ == '__main__':
    main(sys.argv[1:])
