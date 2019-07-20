import unittest
import os,sys,inspect
import logging
import tempfile
from shutil import copyfile, rmtree, copy, copytree, move
import numpy 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import MazeSolverAlgo

# Line Coverage
# branch Coverage
# Condition covera
# Boundarycheck

class CellTest(unittest.TestCase   ):
    def testCellMovementDown(self):
        cell = MazeSolverAlgo.Cell(0,0)
        move = cell.getMoveDownCell( 5 , 5)
        cellTest = MazeSolverAlgo.Cell(1,0)
        self.assertTrue(cellTest == move)
        
        cell = MazeSolverAlgo.Cell(4,4)
        move = cell.getMoveDownCell( 5 , 5)
        self.assertIsNone(move)
        

    def testCellMovementUp(self):
        cell = MazeSolverAlgo.Cell(1,0)
        move = cell.getMoveUpCell( 5 , 5)
        cellTest = MazeSolverAlgo.Cell(0,0)
        self.assertTrue(cellTest == move)
        
        cell = MazeSolverAlgo.Cell(0,0)
        move = cell.getMoveUpCell( 5 , 5)
        self.assertIsNone(move)

    def testCellMovementLeft(self):
        cell = MazeSolverAlgo.Cell(0,1)
        move = cell.getMoveLeftCell( 5 , 5)
        cellTest = MazeSolverAlgo.Cell(0,0)
        self.assertTrue(cellTest == move)
        
        cell = MazeSolverAlgo.Cell(0,0)
        move = cell.getMoveLeftCell( 5 , 5)
        self.assertIsNone(move)

    def testCellMovementRight(self):
        cell = MazeSolverAlgo.Cell(0,0)
        move = cell.getMoveRightCell( 5 , 5)
        cellTest = MazeSolverAlgo.Cell(0,1)
        self.assertTrue(cellTest == move)
        
        cell = MazeSolverAlgo.Cell(4,4)
        move = cell.getMoveRightCell( 5 , 5)
        self.assertIsNone(move)