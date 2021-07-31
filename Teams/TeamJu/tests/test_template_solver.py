
import unittest
import sys
import os
# import pytest

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from TeamJuAlgo import TeamJuAlgo

mg = TeamJuAlgo()

class DImMazeTest(unittest.TestCase):
     def test_setdim(self):
        mazealgo.setDimCols(10)
        mazealgo.setDimRows(99)
        self.assertTrue(mazealgo.dimCols == 10)
        self.assertTrue(mazealgo.dimRows == 99)
        self.assertRaises(Exception, mazealgo.setDimRows, -10)
        self.assertRaises(Exception, mazealgo.setDimCols, -10)
# class FillMazeTest(unittest.TestCase):
#     def test_isingrid(self):
#        self.assertTrue(mg.loadMaze(os.path.realpath(os.path.dirname(
#            __file__))+"/../../../MazeExamples/maze1.txt"))
#        self.assertTrue(mg.isInGrid(0, 0))
