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

class BF_CellisInGridTest(unittest.TestCase):
    def testCelloutsideGrid(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5,5)
        self.assertFalse(bf.isInGrid(10,10))

    def testCellNegoutsideGrid(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5,5)
        self.assertFalse(bf.isInGrid(-2,2))

    def testCellinsideGrid(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5,5)
        self.assertTrue(bf.isInGrid(2,2))

    def testCellonborderRBGrid(self):
        bf = MazeSolverAlgoBreadthFirst()
        astar.startMaze(5,5)
        self.assertTrue(bf.isInGrid(4,4))

    def testCellonborderTLGrid(self):
        bf = MazeSolverAlgoBreadthFirst()
        bf.startMaze(5,5)
        self.assertTrue(bf.isInGrid(0,0))        