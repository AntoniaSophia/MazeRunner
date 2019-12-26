from MazeSolverAlgoBreadthFirst import MazeSolverAlgoBreadthFirst
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


class BF_CellisInGridTest(unittest.TestCase):
    def testCelloutsideGrid(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5, 5)
        self.assertFalse(bf.isInGrid(10, 10))

    def testCellNegoutsideGrid(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5, 5)
        self.assertFalse(bf.isInGrid(-2, 2))

    def testCellinsideGrid(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5, 5)
        self.assertTrue(bf.isInGrid(2, 2))

    def testCellonborderRBGrid(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5, 5)
        self.assertTrue(bf.isInGrid(4, 4))

    def testCellonborderTLGrid(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5, 5)
        self.assertTrue(bf.isInGrid(0, 0))
