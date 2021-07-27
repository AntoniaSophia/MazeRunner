
import unittest
import sys
import os
import pytest

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from SusannaAStarAlgo import SusannaAStarAlgo

mg = SusannaAStarAlgo()


class FillMazeTest(unittest.TestCase):
    def test_isingrid(self):
        self.assertTrue(mg.loadMaze(os.path.realpath(os.path.dirname(
            __file__))+"/../../../MazeExamples/maze1.txt"))
        self.assertTrue(mg.isInGrid(0, 0))
        self.assertFalse(mg.isInGrid(-1, -1))
        self.assertFalse(mg.isInGrid(6, 4))
        self.assertTrue(mg.isInGrid(2, 2))

    def test_getneighbours(self):
        self.assertTrue(mg.loadMaze(os.path.realpath(os.path.dirname(
            __file__))+"/../../../MazeExamples/maze1.txt"))
        solution = [(1, 0), (0, 1)]
        self.assertTrue(solution == mg.getNeighbours(0, 0))
        solution = [(3, 2), (3, 4)]
        self.assertTrue(solution == mg.getNeighbours(3, 3))
        solution = []
        self.assertTrue(solution == mg.getNeighbours(3, 5))

    def test_gridelementtostring(self):
        self.assertTrue(mg.gridElementToString(0, 0) == "0,0")

    def test_isSameGridElement(self):
        self.assertTrue(mg.loadMaze(os.path.realpath(os.path.dirname(
            __file__))+"/../../../MazeExamples/maze1.txt"))
        self.assertTrue(mg.isSameGridElement([0, 0], [0, 0]))
        self.assertTrue(mg.isSameGridElement([4, 4], [4, 4]))
        self.assertFalse(mg.isSameGridElement([0, 1], [1, 0]))

    def test_heuristic(self):
        self.assertTrue(mg.heuristic((0, 1), (1, 0)) == pytest.approx(1.41, 0.01))
        self.assertTrue(mg.heuristic((2, 2), (4, 4)) == pytest.approx(2.82, 0.01))
        self.assertTrue(mg.heuristic((2, 2), (2, 5)) == 3)

    def test_setter(self):
        mg = SusannaAStarAlgo()
        mg.setDimRows(10)
        mg.setDimCols(-10)
        self.assertTrue(mg.dimCols == -10)
        self.assertTrue(mg.dimRows == 10)
        mg.setStartRow(1)
        mg.setStartCol(2)
        mg.setEndCol(3)
        mg.setEndRow(4)
        self.assertTrue(mg.startRow == 1)
        self.assertTrue(mg.startCol == 2)
        self.assertTrue(mg.EndRow == 4)
        self.assertTrue(mg.endCol == 3)
