import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from maze import *
import numpy as np

m = Maze()
val=7
height = int(val/2)
m.create(height, height, Maze.Create.BACKTRACKING)
b = m.maze
b[b == 0] = 2
b[b == 1] = 0
b[b == 2] = 1
(x,y)=b.shape
print(x)
print(b)