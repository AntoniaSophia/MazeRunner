import pytest
import sys
import os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from SusannaAStarAlgo import SusannaAStarAlgo

mg = SusannaAStarAlgo()
mg.loadMaze("..\\..\\MazeExamples\\Maze1.txt")

def test_isingrid():
    assert mg.isInGrid(0,0) == True
    assert mg.isInGrid(-1,-1) == False
    assert mg.isInGrid(6,4) == False
    assert mg.isInGrid(2,2) == True

def test_getneighbours():
    solution = [(1,0),(0,1)]
    assert solution==mg.getNeighbours(0,0)
    solution = [(3,2),(3,4)]
    assert solution==mg.getNeighbours(3,3)
    solution = []
    assert solution==mg.getNeighbours(3,5)

def test_gridelementtostring():
    assert mg.gridElementToString(0,0) == "0,0"

def test_isSameGridElement():
    assert mg.isSameGridElement([0,0], [0,0])
    assert mg.isSameGridElement([4,4], [4,4])
    assert not mg.isSameGridElement([0,1], [1,0])

def test_heuristic():
    assert mg.heuristic((0,1),(1,0))==pytest.approx(1.41,0.01)
    assert mg.heuristic((2,2),(4,4))==pytest.approx(2.82,0.01)
    assert mg.heuristic((2,2),(2,5))==3