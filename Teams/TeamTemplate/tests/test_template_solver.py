
# import unittest
import sys
import os
# import pytest

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from TeamTemplateAlgo import TeamTemplateAlgo

mg = TeamTemplateAlgo()


# class FillMazeTest(unittest.TestCase):
#     def test_isingrid(self):
#        self.assertTrue(mg.loadMaze(os.path.realpath(os.path.dirname(
#            __file__))+"/../../../MazeExamples/maze1.txt"))
#        self.assertTrue(mg.isInGrid(0, 0))
