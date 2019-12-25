from MazeSolverAlgoAStar import MazeSolverAlgoAStar
import unittest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


# Line Coverage
# branch Coverage
# Condition covera
# Boundarycheck


class FillMazeTest(unittest.TestCase):

    def testRefMaze1(self):
        mg = MazeSolverAlgoAStar()

        maze = "maze1.txt"
        refResult = [[0, 4], [0, 3], [0, 2], [0, 1], [0, 0], [1, 0], [2, 0],
                     [3, 0], [4, 0], [4, 1], [4, 2], [3, 2], [3, 3], [3, 4], [2, 4]]

        mg.loadMaze(os.path.join(currentdir, "..", "..", "..", "MazeExamples", maze))
        result = mg.solveMaze()
        self.assertTrue(result == refResult)

    def testRefMaze2(self):
        mg = MazeSolverAlgoAStar()

        maze = "maze2.txt"
        refResult = [[3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1],
                     [9, 2], [9, 3], [9, 4], [9, 5], [8, 5], [8, 6], [8, 7], [8, 8]]

        mg.loadMaze(os.path.join(currentdir, "..", "..", "..", "MazeExamples", maze))
        result = mg.solveMaze()
        self.assertTrue(result == refResult)

    def testSetStartEndCol(self):
        mg = MazeSolverAlgoAStar()
        maze = "maze2.txt"
        mg.loadMaze(os.path.join(currentdir, "..", "..", "..", "MazeExamples", maze))

        mg.setStartCol(-1)
        self.assertTrue(mg.startCol == -1)

        mg.setStartRow(-1)
        self.assertTrue(mg.startRow == -1)

        mg.setEndCol(-1)
        self.assertTrue(mg.endCol == -1)

        mg.setEndRow(-1)
        self.assertTrue(mg.endRow == -1)

    def testSetBlocked(self):
        mg = MazeSolverAlgoAStar()
        maze = "maze2.txt"
        mg.loadMaze(os.path.join(currentdir, "..", "..", "..", "MazeExamples", maze))

        mg.setBlocked(0, 0)

        self.assertTrue(mg.grid[0][0] == mg.OBSTACLE)
