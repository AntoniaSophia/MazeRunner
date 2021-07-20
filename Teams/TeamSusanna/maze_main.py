from tkinter import StringVar, Label, Canvas, Tk, IntVar
import SusannaAStarAlgo
import sys
import threading
import os

sys.path.append("../..")
import Framework.Visualizer.maze_visualize

def on_closing():
    os._exit(0)

apptk = Tk()
apptk.protocol("WM_DELETE_WINDOW", on_closing)
apptk.title("MazeRunner")
apptk.geometry("700x700")
apptk.resizable(True, True)

alg = SusannaAStarAlgo.SusannaAStarAlgo()
vis = Framework.Visualizer.maze_visualize.MazeVisualizer(apptk)


if not alg.loadMaze("ascii_image.txt"):
    exit(1)

print("[TeamTemplateAlgo]: loaded maze\n", alg.grid)

vis.clearMaze()
vis.setDimRowsCmd(alg.dimRows)
vis.setDimColsCmd(alg.dimCols)
vis.startMaze(vis.columns, vis.rows)
vis.setStartCol(alg.startCol)
vis.setEndCol(alg.endCol)
vis.setStartRow(alg.startRow)
vis.setEndRow(alg.endRow)
vis.initialize_grid(False)

for row in range(alg.dimRows):
    for col in range(alg.dimCols):
        if alg.grid[row][col]==alg.OBSTACLE:
            vis.setBlocked(row,col)

vis.endMaze()

def mainloop():
    solutionString = alg.solveMaze()
    print("[TeamTemplateAlgo]: Result of solving maze: ", solutionString)
    for move in alg.resultpath:
        vis.addSolutionStep(move[0],move[1])    

t = threading.Thread(target=mainloop)
t.start()

apptk.mainloop()