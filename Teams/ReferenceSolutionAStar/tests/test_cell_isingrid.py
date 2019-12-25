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


class CellisInGridTest(unittest.TestCase):
    def testCelloutsideGrid(self):
        astar = MazeSolverAlgoAStar()
        astar.startMaze(5, 5)
        self.assertFalse(astar.isInGrid(10, 10))

    def testCellNegoutsideGrid(self):
        astar = MazeSolverAlgoAStar()
        astar.startMaze(5, 5)
        self.assertFalse(astar.isInGrid(-2, 2))

    def testCellinsideGrid(self):
        astar = MazeSolverAlgoAStar()
        astar.startMaze(5, 5)
        self.assertTrue(astar.isInGrid(2, 2))

    def testCellonborderRBGrid(self):
        astar = MazeSolverAlgoAStar()
        astar.startMaze(5, 5)
        self.assertTrue(astar.isInGrid(4, 4))

    def testCellonborderTLGrid(self):
        astar = MazeSolverAlgoAStar()
        astar.startMaze(5, 5)
        self.assertTrue(astar.isInGrid(0, 0))
