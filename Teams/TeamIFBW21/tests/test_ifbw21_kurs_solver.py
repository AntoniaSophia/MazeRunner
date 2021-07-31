
import unittest
import sys
import os
# import pytest

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from IFBW21Algo import IFBW21Algo

mazealgo = IFBW21Algo()


class DimMazeTest(unittest.TestCase):

    def test_setdim(self):
        mazealgo.setDimCols(10)
        mazealgo.setDimRows(99)
        self.assertTrue(mazealgo.dimCols == 10)
        self.assertTrue(mazealgo.dimRows == 99)
        self.assertRaises(Exception, mazealgo.setDimRows, -10)
        self.assertRaises(Exception, mazealgo.setDimCols, -10)


class MazeLoadTest(unittest.TestCase):
    def test_loadmaze_fileload(self):
        self.assertTrue(mazealgo.loadMaze(os.path.realpath(
            os.path.dirname(__file__)) + "/../../../MazeExamples/maze1.txt"))
        self.assertFalse(mazealgo.loadMaze(os.path.realpath(
            os.path.dirname(__file__)) + "/../../../MazeExamples/maze9.txt"))

    def test_loadmaze_dimension(self):
        mazealgo.loadMaze(os.path.realpath(
            os.path.dirname(__file__)) + "/../../../MazeExamples/maze1.txt")
        self.assertTrue(mazealgo.dimRows == 6)
        self.assertTrue(mazealgo.dimCols == 5)

    def test_loadmaze_startpos(self):
        mazealgo.loadMaze(os.path.realpath(
            os.path.dirname(__file__)) + "/../../../MazeExamples/maze1.txt")
        self.assertTrue(mazealgo.startRow == 0)
        self.assertTrue(mazealgo.startCol == 4)

    def test_loadmaze_endpos(self):
        mazealgo.loadMaze(os.path.realpath(
            os.path.dirname(__file__)) + "/../../../MazeExamples/maze1.txt")
        self.assertTrue(mazealgo.endRow == 2)
        self.assertTrue(mazealgo.endCol == 4)

    def test_loadmaze_isingrid(self):
        mazealgo.loadMaze(os.path.realpath(
            os.path.dirname(__file__)) + "/../../../MazeExamples/maze1.txt")
        self.assertTrue(mazealgo.isInGrid(column=4, row=5))
        self.assertFalse(mazealgo.isInGrid(4, 5))
        self.assertTrue(mazealgo.isInGrid(row=4, column=4))

    def test_loadmaze_broken(self):
        self.assertFalse(mazealgo.loadMaze(os.path.realpath(
            os.path.dirname(__file__)) + "/../../../MazeExamples/maze1_broken.txt"))


class MazeNeighbours(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MazeNeighbours, self).__init__(*args, **kwargs)
        mazealgo.loadMaze(os.path.realpath(
            os.path.dirname(__file__)) + "/../../../MazeExamples/maze1.txt")

    def test_neighbour_up(self):
        lResultArr = mazealgo.getNeighbours(0, 0)
        self.assertTrue(len(lResultArr) == 2)

    def test_neighbours(self):
        lResultArr = mazealgo.getNeighbours(3, 2)
        self.assertTrue(len(lResultArr) == 3)
        print(lResultArr)
        self.assertTrue(lResultArr == [(2, 2), (4, 2), (3, 3)])

        lResultArr = mazealgo.getNeighbours(5, 4)
        self.assertTrue(len(lResultArr) == 2)
        self.assertTrue(lResultArr == [(4, 4), (5, 3)])


class MazeMiscFunctions(unittest.TestCase):
    def test_neighbours(self):
        self.assertTrue(mazealgo.gridElementToString(1, 2) == "1-2")
        self.assertTrue(mazealgo.gridElementToString(1123213, 223234234) == "1123213-223234234")

    def test_isSameGridElement(self):
        self.assertFalse(mazealgo.isSameGridElement([2, 1], [1, 2]))
        self.assertTrue(mazealgo.isSameGridElement([100, 101], [100, 101]))

    def test_heuristic(self):
        self.assertAlmostEqual(mazealgo.heuristic([2, 1], [1, 2]), 2)


class MazeSolver(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MazeSolver, self).__init__(*args, **kwargs)
        mazealgo.loadMaze(os.path.realpath(
            os.path.dirname(__file__)) + "/../../../MazeExamples/maze1.txt")

    def test_solvemaze(self):
        solvepath = mazealgo.solveMaze()
        self.assertTrue([(0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0),
                         (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (3, 2),
                         (3, 3), (3, 4), (2, 4)], solvepath)
