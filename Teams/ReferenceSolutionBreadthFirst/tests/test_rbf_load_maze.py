from MazeSolverAlgoBreadthFirst import MazeSolverAlgoBreadthFirst
import unittest
import os
import sys
import inspect
import numpy
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


# Line Coverage
# branch Coverage
# Condition covera
# Boundarycheck


class BF_LoadMazeTest(unittest.TestCase):
    def testLoadMaze(self):
        example_load = os.path.join(parentdir, "..", "..", "MazeExamples", "maze1.txt")
        bf = MazeSolverAlgoBreadthFirst()
        bf.loadMaze(example_load)
        result = numpy.array([[0, 0, 0, 0, 2], [0, 1, 1, 1, 1], [0, 1, 0, 1, 3], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [0,0,0,0,0]])
        # self.assertTrue(astar.grid == result)
        numpy.testing.assert_array_equal(bf.grid, result)


if __name__ == '__main__':
    unittest.main()
