import unittest
import os,sys,inspect
import logging
import tempfile
from shutil import copyfile, rmtree, copy, copytree, move
import numpy 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import maze_generator_algo 

# Line Coverage
# branch Coverage
# Condition covera
# Boundarycheck

class GeneratorTest(unittest.TestCase   ):
    def testSetUp(self):
        dimensionRow = 5
        dimensionCol = 5 
        complexity = 1
        density = 1

        genalgo = maze_generator_algo.MazeGeneratorAlgo(dimensionRow, dimensionCol,complexity, density)
        genalgo.createMaze()
        res = [1, 1, 1, 1, 1]
        self.assertTrue(numpy.alltrue(res == genalgo.grid[0]))
        self.assertTrue(numpy.alltrue(res == genalgo.grid[-1]))

        genalgo.grid = numpy.transpose(genalgo.grid)
        self.assertTrue(numpy.alltrue(res == genalgo.grid[0]))
        self.assertTrue(numpy.alltrue(res == genalgo.grid[-1]))        