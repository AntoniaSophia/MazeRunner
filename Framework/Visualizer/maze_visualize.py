from tkinter import StringVar, Label, Canvas, Tk, IntVar
import os
import sys
import math
import numpy
import paho.mqtt.client as mqtt


if "MQTTSERVER" in os.environ and os.environ['MQTTSERVER']:
    mqtt_server = os.environ['MQTTSERVER']
else:
    mqtt_server = "127.0.0.1"


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


class MqttClient:
    """contains Code from Nikos Kanargias <nkana@tee.gr>"""

    def onMessage(self, master, obj, msg):
        # pylint: disable=unused-argument
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))
        print("[MazeVisualizer]: Received message: ", topic, " --> ", payload)
        if topic == "/maze":
            if payload == "clear":
                self.mazeVisualizer.clearMaze()
            elif payload == "start":
                self.mazeVisualizer.startMaze()
            elif payload == "end":
                self.mazeVisualizer.endMaze()
            else:
                pass
        elif topic == "/maze/dimRow":
            self.mazeVisualizer.setDimRowsCmd(int(payload))
            self.mazeVisualizer.startMaze(
                self.mazeVisualizer.columns, self.mazeVisualizer.rows)
        elif topic == "/maze/dimCol":
            self.mazeVisualizer.setDimColsCmd(int(payload))
            self.mazeVisualizer.startMaze(
                self.mazeVisualizer.columns, self.mazeVisualizer.rows)
        elif topic == "/maze/startCol":
            self.mazeVisualizer.setStartCol(int(payload))
        elif topic == "/maze/startRow":
            self.mazeVisualizer.setStartRow(int(payload))
        elif topic == "/maze/endCol":
            self.mazeVisualizer.setEndCol(int(payload))
        elif topic == "/maze/endRow":
            self.mazeVisualizer.setEndRow(int(payload))
            self.mazeVisualizer.initialize_grid(
                False)    # initialize the new grid!!!
        elif topic == "/maze/blocked":
            cell = payload.split(",")
            self.mazeVisualizer.setBlocked(int(cell[0]), int(cell[1]))
        elif topic == "/maze/go":
            cell = payload.split(",")
            self.mazeVisualizer.addSolutionStepFin(int(cell[0]), int(cell[1]))

        else:
            pass

    def onConnect(self, master, obj, flags, rc):
        # pylint: disable=unused-argument
        self.master.subscribe("/maze")
        self.master.subscribe("/maze/dimRow")
        self.master.subscribe("/maze/dimCol")
        self.master.subscribe("/maze/startCol")
        self.master.subscribe("/maze/startRow")
        self.master.subscribe("/maze/endCol")
        self.master.subscribe("/maze/endRow")
        self.master.subscribe("/maze/blocked")
        self.master.subscribe("/maze/go")

        print("[MazeVisualizer]: Connnect to mqtt-broker")

    def __init__(self, master, appl):
        self.master = master
        self.master.on_connect = self.onConnect
        self.master.on_message = self.onMessage
        self.master.connect(mqtt_server, 1883, 60)
        self.mazeVisualizer = MazeVisualizer(appl)


class MazeVisualizer:
    # pylint: disable=no-member
    class Cell(object):
        """
        Helper class that represents the cell of the grid
        """

        def __init__(self, row, col):
            self.row = row  # the row number of the cell(row 0 is the top)
            # the column number of the cell (column 0 is the left)
            self.col = col
            self.prev = self.__class__

        def __eq__(self, other):
            """
            useful Cell equivalence
            """
            if isinstance(other, self.__class__):
                return self.row == other.row and self.col == other.col
            else:
                return False

    class Point(object):
        """
        Helper class that represents the point on the grid
        """

        def __init__(self, x, y):
            self.X = x
            self.Y = y

        def get_x(self):
            return self.X

        def get_y(self):
            return self.Y

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

    def setDimRowsCmd(self, rows):
        self.rows = rows

    def setDimColsCmd(self, cols):
        self.columns = cols

    def setStartCol(self, col):
        self.robotStart_col = col

    def setStartRow(self, row):
        self.robotStart_row = row

    def setEndCol(self, col):
        self.targetPos_col = col

    def setEndRow(self, row):
        self.targetPos_row = row

    def setBlocked(self, row, col):
        self.grid[row][col] = 1

    def startMaze(self, columns=0, rows=0):
        self.setDimCols = 0
        self.setDimRows = 0
        self.setStartCols = 0
        self.setStartRows = 0
        self.setEndCols = 0
        self.setEndRows = 0
        self.grid = [[]]

        if columns > 0 and rows > 0:
            self.grid = numpy.empty((rows, columns), dtype=int)
            for i in range(rows):
                for j in range(columns):
                    self.grid[i][j] = 0

    def endMaze(self):
        self.grid[self.targetPos_row][self.targetPos_col] = self.TARGET
        self.grid[self.robotStart_row][self.robotStart_col] = self.ROBOT
        self.targetPos = self.Cell(self.targetPos_row, self.targetPos_col)
        self.robotStart = self.Cell(self.robotStart_row, self.robotStart_col)
        # print("Following Maze received: ")
        # self.printMaze()
        self.repaint()

    def printMaze(self):
        print(self.grid)

    def addSolutionStepFin(self, row, col):
        step = self.Cell(row, col)
        self.closedSet2.append(step)
        # print("Step")
        if step == self.targetPos:
            print("Finished")
            self.plot_route(True)

    def addSolutionStep(self, row, col):
        step = self.Cell(row, col)
        self.closedSet.append(step)
        # print("Step")

    def __init__(self, maze):
        """
        Constructor
        """
        self.maze = maze
        self.center(maze)
        self.rows = 9               # the number of rows of the grid
        self.columns = 9            # the number of columns of the grid
        self.initVar()
        self.initialize_grid(True)
        self.repaint()

    def initVar(self):
        self.square_size = 0        # the cell size in pixels
        # the size of the tips of the arrow pointing the predecessor cell
        self.arrow_size = 0

        self.radius = 0.0           # the radius of triangular and hexagonal cells
        # half the height of hexagonal cells or the height of triangular cells
        self.height = 0.0
        self.edge = 0.0             # the edge of the triangular cell

        self.openSet = []           # the OPEN SET
        self.closedSet = []         # the CLOSED SET
        self.closedSet2 = []         # the CLOSED SET
        # the set of vertices of the graph to be explored by Dijkstra's algorithm
        self.graph = []

        self.robotStart_col = 0
        self.robotStart_row = 0
        self.targetPos_col = self.rows - 5
        self.targetPos_row = self.columns - 5

        self.robotStart = self.Cell(self.robotStart_row, self.robotStart_col)
        self.targetPos = self.Cell(self.targetPos_row, self.targetPos_col)

        self.grid = [[]]            # the grid
        self.centers = [[self.Point(0, 0) for c in range(83)]
                        for r in range(83)]  # the centers of the cells
        # distance of the point the user clicked on the canvas from the centre of some cell
        self.dist = self.INFINITY
        self.realTime = False       # Solution is displayed instantly
        self.found = False          # flag that the goal was found
        self.searching = False      # flag that the search is in progress
        self.endOfSearch = False    # flag that the search came to an end
        self.animation = False      # flag that the animation is running
        self.delay = 500            # time delay of animation (in msec)
        self.expanded = 0           # the number of nodes that have been expanded
        self.shape = "Square"       # Square is initially selected
        self.algorithm = "DFS"      # DFS is initially selected

        self.array = numpy.array([0] * (83 * 83))
        self.cur_row = self.cur_col = self.cur_val = 0
        self.message_var = StringVar()
        self.message = Label(self.maze, width=55, anchor='w',
                             font=('Helvetica', 8), fg="black", textvariable=self.message_var)

        self.message.place(x=5, y=920)

        self.rows_var = StringVar()
        self.rows_var.set(41)
        self.cols_var = StringVar()
        self.cols_var.set(41)

        self.drawArrows = IntVar()

        self.canvas = Canvas(self.maze, bd=0, highlightthickness=0)

    def initialize_grid(self, make_maze):
        """
        Creates a new clean grid or a new maze

        :param make_maze: flag that indicates the creation of a random maze
        """

        # the columns of the square maze must be equal to rows
        if make_maze and self.shape == "Square":
            self.columns = self.rows
            self.cols_var.set(self.columns)
            self.grid = self.array[:self.rows*self.columns]
            self.grid = self.grid.reshape(self.rows, self.columns)

            for r in range(self.rows):
                for c in list(range(self.columns)):
                    self.grid[r][c] = self.EMPTY

        # Calculation of the size of the square cell
        if self.shape == "Square":
            self.square_size = int(
                700 / (self.rows if self.rows > self.columns else self.columns))
            self.arrow_size = int(self.square_size / 2)

        if self.shape == "Square":
            self.canvas.configure(
                width=self.columns * self.square_size + 1, height=self.rows * self.square_size + 1)
            self.canvas.place(x=10, y=10)
            self.canvas.create_rectangle(0, 0, self.columns*(self.square_size+1),
                                         self.rows*(self.square_size+1), width=0, fill="DARK GREY")
            self.canvas.create_rectangle(
                0, 0, 950, 950, width=0, fill="DARK GREY")

        # Calculation of the coordinates of the cells' centers
        y = 0
        for r in range(self.rows):
            for c in range(self.columns):
                if self.shape == "Triangle":
                    if (c % 2 == 0 and r % 2 == 0) or (c % 2 != 0 and r % 2 != 0):
                        y = round(r*self.height + self.height/3)
                    if (c % 2 == 0 and r % 2 != 0) or (c % 2 != 0 and r % 2 == 0):
                        y = round(r * self.height + self.height*2/3)
                    self.centers[r][c] = self.Point(
                        round((c + 1) / 2.0 * self.edge), y)
                if self.shape == "Square":
                    self.centers[r][c] = self.Point(c*self.square_size+self.square_size/2,
                                                    r*self.square_size+self.square_size/2)
                if self.shape == "Hexagon":
                    if c % 2 == 0:
                        self.centers[r][c] = self.Point(round((int(c/2)*3+1)*self.radius),
                                                        round((r*2+1)*self.height))
                    else:
                        self.centers[r][c] = self.Point(round(self.radius/2+(int(c/2)*3+2)*self.radius),
                                                        round(2*(r+1)*self.height))

    def repaint(self):
        """
        Repaints the grid
        """
        color = ""
        # print("repaint")
        for r in range(self.rows):
            for c in range(self.columns):
                # print (self.grid[r][c])
                if self.grid[r][c] == self.EMPTY:
                    color = "WHITE"
                elif self.grid[r][c] == self.ROBOT:
                    color = "RED"
                elif self.grid[r][c] == self.TARGET:
                    color = "GREEN"
                elif self.grid[r][c] == self.OBST:
                    color = "BLACK"
                elif self.grid[r][c] == self.FRONTIER:
                    color = "BLUE"
                elif self.grid[r][c] == self.CLOSED:
                    color = "CYAN"
                elif self.grid[r][c] == self.ROUTE:
                    color = "YELLOW"
                self.paint_cell(r, c, color)

    def paint_cell(self, row, col, color):
        """
        Paints a particular cell

        :param row:   the row of the cell
        :param col:   the column of the cell
        :param color: the color of the cell
        """
        if self.shape == "Square":
            self.canvas.create_polygon(
                self.calc_square(row, col), width=0, fill=color)

    def calc_square(self, r, c):
        """
        Calculates the coordinates of the vertices of the square corresponding to a particular cell

        :param r:   the row of the cell
        :param c:   the column of the cell
        :return :   List of the pairs of coordinates
        """
        polygon = []
        polygon.extend((c*self.square_size + 1, r*self.square_size + 1))
        polygon.extend(((c+1)*self.square_size + 0,
                       r*self.square_size + 1))
        polygon.extend(((c+1)*self.square_size + 0,
                       (r+1)*self.square_size + 0))
        polygon.extend((c*self.square_size + 1, (r+1)*self.square_size + 0))
        return polygon

    def maze_click(self):
        """
        Action performed when user clicks "Maze" button
        """
        # pylint: disable=no-member
        self.animation = False
        self.realTime = False
        for but in self.buttons:
            but.configure(state="normal")
        self.buttons[3].configure(fg="BLACK")  # Real-Time button
        self.slider.configure(state="normal")
        for but in self.algo_buttons:
            but.configure(state="normal")
        self.diagonalBtn.configure(state="normal")
        self.drawArrowsBtn.configure(state="normal")
        self.initialize_grid(True)
        if self.shape == "Triangle":
            self.diagonalBtn.configure(state="disabled")

    def clearMaze(self):
        """
        Action performed when user clicks "Clear" button
        """
        self.canvas.delete("all")
        self.initVar()
        self.initialize_grid(True)

    def check_termination(self):
        """
        Checks if search is completed
        """
        # Here we decide whether we can continue the search or not.
        # In the case of DFS, BFS, A* and Greedy algorithms
        # here we have the second step:
        # 2. If OPEN SET = [], then terminate. There is no solution.
        if (self.algorithm == "Dijkstra" and not self.graph) or\
                self.algorithm != "Dijkstra" and not self.openSet:
            self.endOfSearch = True
            self.grid[self.robotStart.row][self.robotStart.col] = self.ROBOT
            self.message.configure(text=self.MSG_NO_SOLUTION)
            self.buttons[4].configure(
                state="disabled")     # Step-by-Step button
            self.buttons[5].configure(state="disabled")     # Animation button
            self.slider.configure(state="disabled")
            self.repaint()
            if self.drawArrows.get():
                self.draw_arrows()
        else:
            self.expand_node()
            if self.found:
                self.endOfSearch = True
                self.plot_route()
                self.buttons[4].configure(
                    state="disabled")  # Step-by-Step button
                self.buttons[5].configure(state="disabled")  # Animation button
                self.slider.configure(state="disabled")

    def prepareVisualization(self, dimrows, dimcols, startrow, startcol, endrow, endcol):
        self.clearMaze()
        self.setDimRowsCmd(dimrows)
        self.setDimColsCmd(dimcols)
        self.startMaze(self.columns, self.rows)
        self.setStartCol(startcol)
        self.setEndCol(endcol)
        self.setStartRow(startrow)
        self.setEndRow(endrow)
        self.initialize_grid(False)

    def plot_route(self, fin=False, font=False):
        """
                Calculates the path from the target to the initial position of the robot,
        counts the corresponding steps and measures the distance traveled.
        """
        # self.repaint()
        self.searching = False
        steps = 0
        if fin:
            closedSet = self.closedSet2
        else:
            closedSet = self.closedSet

        # print(len(self.closedSet))
        stepcol = 255/len(closedSet)
        step_colpos = 0.0
        cur = closedSet[0]
        step_pos = 1
        for cur in closedSet:
            if self.targetPos == cur:
                break
            self.grid[cur.row][cur.col] = self.ROUTE
            if fin:
                self.paint_cell(cur.row, cur.col, _from_rgb(
                    (255, int(step_colpos), 255-int(step_colpos))))
                canvas_id = self.canvas.create_text(
                    cur.col*self.square_size, cur.row*self.square_size,
                    anchor="nw", font=("Courier", 6), fill=_from_rgb((0, 10, 100)))
                if font:
                    self.canvas.itemconfig(canvas_id, text=str(step_pos))
            else:
                self.paint_cell(cur.row, cur.col, _from_rgb(
                    (10, int(step_colpos), 255-int(step_colpos))))
                canvas_id = self.canvas.create_text(
                    cur.col*self.square_size,
                    cur.row*self.square_size,
                    anchor="nw", font=("Courier", 6), fill=_from_rgb((0, 10, 100)))
                if font:
                    self.canvas.itemconfig(canvas_id, text=str(step_pos))
            step_pos += 1
            step_colpos += stepcol
            # if cur != old:
            #     self.draw_arrow(old, cur, self.arrow_size, "GREY", 2 if self.arrow_size >= 10 else 1)
        self.grid[self.robotStart.row][self.robotStart.col] = self.ROBOT
        self.paint_cell(self.robotStart.row, self.robotStart.col, "RED")

        msg = "Nodes Steps: {}".format(steps)
        self.message_var.set(msg)

    def find_connected_component(self, v):
        """
        Appends to the list containing the nodes of the graph only
                the cells belonging to the same connected component with node v.
        :param v: the starting node
        """
        # This is a Breadth First Search of the graph starting from node v.
        stack = [v]
        self.graph.append(v)
        while stack:
            v = stack.pop()
            successors = self.create_successors(v, True)
            for c in successors:
                if c not in self.graph:
                    stack.append(c)
                    self.graph.append(c)

    def draw_arrows(self):
        """
        Draws the arrows to predecessors
        """
        # We draw black arrows from each open or closed state to its predecessor.
        for r in range(self.rows):
            for c in range(self.columns):
                tail = head = cell = self.Cell(r, c)
                # If the current cell is an open state, or is a closed state
                # but not the initial position of the robot
                if self.grid[r][c] in [self.FRONTIER, self.CLOSED, self.ROUTE] and not cell == self.robotStart:
                    # The tail of the arrow is the current cell, while
                    # the arrowhead is the predecessor cell.
                    if self.grid[r][c] == self.FRONTIER:
                        if self.algorithm == "Dijkstra":
                            tail = self.graph[self.graph.index(cell)]
                            head = tail.prev
                        else:
                            tail = self.openSet[self.openSet.index(cell)]
                            head = tail.prev
                    elif self.grid[r][c] == self.ROUTE:
                        tail = self.closedSet[self.closedSet.index(cell)]
                        head = tail.prev

                    self.draw_arrow(tail, head, self.arrow_size,
                                    "BLACK", 2 if self.arrow_size >= 10 else 1)

        if self.found:
            # We draw red arrows along the path from robotStart to targetPos.
            # index = self.closedSet.index(self.targetPos)
            cur = self.closedSet[self.closedSet.index(self.targetPos)]
            while cur != self.robotStart:
                head = cur
                cur = cur.prev
                tail = cur
                self.draw_arrow(tail, head, self.arrow_size,
                                "RED", 2 if self.arrow_size >= 10 else 1)

    def draw_arrow(self, tail, head, a, color, width):
        """
        Draws an arrow from center of tail cell to center of head cell

        :param tail:   the tail of the arrow
        :param head:   the head of the arrow
        :param a:      size of arrow tips
        :param color:  color of the arrow
        :param width:  thickness of the lines
        """
        # The coordinates of the center of the tail cell
        x1 = self.centers[tail.row][tail.col].get_x()
        y1 = self.centers[tail.row][tail.col].get_y()
        # The coordinates of the center of the head cell
        x2 = self.centers[head.row][head.col].get_x()
        y2 = self.centers[head.row][head.col].get_y()

        sin20 = math.sin(20*math.pi/180)
        cos20 = math.cos(20*math.pi/180)
        sin25 = math.sin(25*math.pi/180)
        cos25 = math.cos(25*math.pi/180)
        sin10 = math.sin(10*math.pi/180)
        cos10 = math.cos(10*math.pi/180)
        sin40 = math.sin(40*math.pi/180)
        cos40 = math.cos(40*math.pi/180)
        u3 = v3 = u4 = v4 = 0

        if x1 == x2 and y1 > y2:  # up
            u3 = x2 - a*sin20
            v3 = y2 + a*cos20
            u4 = x2 + a*sin20
            v4 = v3
        elif x1 < x2 and y1 > y2 and self.shape == "Square":  # up-right square cell
            u3 = x2 - a*cos25
            v3 = y2 + a*sin25
            u4 = x2 - a*sin25
            v4 = y2 + a*cos25
        # up-right triangular and hexagonal cells
        elif x1 < x2 and y1 > y2 and self.shape in ["Triangle", "Hexagon"]:
            u3 = x2 - a * cos10
            v3 = y2 + a * sin10
            u4 = x2 - a * sin40
            v4 = y2 + a * cos40
        elif x1 < x2 and y1 == y2:  # right
            u3 = x2 - a*cos20
            v3 = y2 - a*sin20
            u4 = u3
            v4 = y2 + a*sin20
        elif x1 < x2 and y1 < y2 and self.shape == "Square":  # right-down square cell
            u3 = x2 - a*cos25
            v3 = y2 - a*sin25
            u4 = x2 - a*sin25
            v4 = y2 - a*cos25
        # right-down triangular and hexagonal cells
        elif x1 < x2 and y1 < y2 and self.shape in ["Triangle", "Hexagon"]:
            u3 = x2 - a * cos10
            v3 = y2 - a * sin10
            u4 = x2 - a * sin40
            v4 = y2 - a * cos40
        elif x1 == x2 and y1 < y2:  # down
            u3 = x2 - a*sin20
            v3 = y2 - a*cos20
            u4 = x2 + a*sin20
            v4 = v3
        elif x1 > x2 and y1 < y2 and self.shape == "Square":  # left-down square cell
            u3 = x2 + a*sin25
            v3 = y2 - a*cos25
            u4 = x2 + a*cos25
            v4 = y2 - a*sin25
        # left-down triangular and hexagonal cells
        elif x1 > x2 and y1 < y2 and self.shape in ["Triangle", "Hexagon"]:
            u3 = x2 + a * sin40
            v3 = y2 - a * cos40
            u4 = x2 + a * cos10
            v4 = y2 - a * sin10
        elif x1 > x2 and y1 == y2:  # left
            u3 = x2 + a*cos20
            v3 = y2 - a*sin20
            u4 = u3
            v4 = y2 + a*sin20
        elif x1 > x2 and y1 > y2 and self.shape == "Square":  # left-up square cell
            u3 = x2 + a*sin25
            v3 = y2 + a*cos25
            u4 = x2 + a*cos25
            v4 = y2 + a*sin25
        # left-up triangular and hexagonal cells
        elif x1 > x2 and y1 > y2 and self.shape in ["Triangle", "Hexagon"]:
            u3 = x2 + a*sin40
            v3 = y2 + a*cos40
            u4 = x2 + a*cos10
            v4 = y2 + a*sin10

        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        self.canvas.create_line(x2, y2, u3, v3, fill=color, width=width)
        self.canvas.create_line(x2, y2, u4, v4, fill=color, width=width)

    @staticmethod
    def center(window):
        """
        Places a window at the center of the screen
        """
        window.update_idletasks()
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        size = tuple(int(_)
                     for _ in window.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        window.geometry("%dx%d+%d+%d" % (size + (x, y)))


def on_closing():
    os._exit(0)


if __name__ == '__main__':
    app = Tk()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.title("MazeRunner")
    app.geometry("700x700")
    app.resizable(True, True)

    mqttclient = mqtt.Client()
    ob1 = MqttClient(mqttclient, app)
    mqttclient.loop_start()
    app.mainloop()
