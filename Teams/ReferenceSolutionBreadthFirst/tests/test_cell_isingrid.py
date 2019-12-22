import unittest
import pytest
import os,sys,inspect
import logging
import tempfile
from shutil import copyfile, rmtree, copy, copytree, move
import numpy 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from MazeSolverAlgoBreadthFirst import MazeSolverAlgoBreadthFirst

# Line Coverage
# branch Coverage
# Condition covera
# Boundarycheck

class CellisInGridTest(unittest.TestCase):
    def testCelloutsideGrid(self):
        astar = MazeSolverAlgoBreadthFirst()
        astar.startMaze(5,5)
        self.assertFalse(astar.isInGrid(10,10))

    def testCellNegoutsideGrid(self):
        astar = MazeSolverAlgoBreadthFirst()
        astar.startMaze(5,5)
        self.assertFalse(astar.isInGrid(-2,2))

    def testCellinsideGrid(self):
        astar = MazeSolverAlgoBreadthFirst()
        astar.startMaze(5,5)
        self.assertTrue(astar.isInGrid(2,2))

    def testCellonborderRBGrid(self):
        astar = MazeSolverAlgoBreadthFirst()
        astar.startMaze(5,5)
        self.assertTrue(astar.isInGrid(4,4))

    def testCellonborderTLGrid(self):
        astar = MazeSolverAlgoBreadthFirst()
        astar.startMaze(5,5)
        self.assertTrue(astar.isInGrid(0,0))        