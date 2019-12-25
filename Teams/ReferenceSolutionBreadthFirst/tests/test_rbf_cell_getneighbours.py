import unittest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from MazeSolverAlgoBreadthFirst import MazeSolverAlgoBreadthFirst  # noqa: E402

# Line Coverage
# branch Coverage
# Condition covera
# Boundarycheck


class BF_CellGetNeighboursTest(unittest.TestCase):
    def testCellGetNeighbours(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5, 5)
        neighbors = bf.getNeighbours(2, 2)
        result = [[3, 2], [1, 2], [2, 3], [2, 1]]
        self.assertTrue(neighbors == result)

    def testCellGetNeighboursBordersRB(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5, 5)
        neighbors = bf.getNeighbours(4, 4)
        result = [[3, 4], [4, 3]]
        self.assertTrue(neighbors == result)

    def testCellGetNeighboursBordersLT(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5, 5)
        neighbors = bf.getNeighbours(0, 0)
        result = [[1, 0], [0, 1]]
        self.assertTrue(neighbors == result)

    def testCellGetNeighboursBordersLB(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5, 5)
        neighbors = bf.getNeighbours(0, 4)
        result = [[1, 4], [0, 3]]
        self.assertTrue(neighbors == result)

    def testCellGetNeighboursBordersRT(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5, 5)
        neighbors = bf.getNeighbours(4, 0)
        result = [[3, 0], [4, 1]]
        self.assertTrue(neighbors == result)

    # def testCellMovementUp(self):
    #     cell = MazeSolverAlgoAStar.Cell(1,0)
    #     move = cell.getMoveUpCell( 5 , 5)
    #     cellTest = MazeSolverAlgoAStar.Cell(0,0)
    #     self.assertTrue(cellTest == move)

    #     cell = MazeSolverAlgoAStar.Cell(0,0)
    #     move = cell.getMoveUpCell( 5 , 5)
    #     self.assertIsNone(move)

    # def testCellMovementLeft(self):
    #     cell = MazeSolverAlgoAStar.Cell(0,1)
    #     move = cell.getMoveLeftCell( 5 , 5)
    #     cellTest = MazeSolverAlgoAStar.Cell(0,0)
    #     self.assertTrue(cellTest == move)

    #     cell = MazeSolverAlgoAStar.Cell(0,0)
    #     move = cell.getMoveLeftCell( 5 , 5)
    #     self.assertIsNone(move)

    # def testCellMovementRight(self):
    #     cell = MazeSolverAlgoAStar.Cell(0,0)
    #     move = cell.getMoveRightCell( 5 , 5)
    #     cellTest = MazeSolverAlgoAStar.Cell(0,1)
    #     self.assertTrue(cellTest == move)

    #     cell = MazeSolverAlgoAStar.Cell(4,4)
    #     move = cell.getMoveRightCell( 5 , 5)
    #     self.assertIsNone(move)
