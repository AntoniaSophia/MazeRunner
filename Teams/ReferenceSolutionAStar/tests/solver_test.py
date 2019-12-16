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

from MazeSolverAlgoAStar import MazeSolverAlgoAStar

# Line Coverage
# branch Coverage
# Condition covera
# Boundarycheck

class CellTest(unittest.TestCase):
    def testCellGetNeighbours(self):
        astar = MazeSolverAlgoAStar()
        astar.startMaze(5,5)
        neighbors = astar.getNeighbours(2,2)
        result = [[3, 2], [1, 2], [2, 3], [2, 1]]
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