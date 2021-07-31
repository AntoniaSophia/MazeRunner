"""Maze solver algorithm test script

This script allows the user to load an maze from text, execute the maze solver and
visualize the maze and solution path using tkinter
"""
from tkinter import Tk
import argparse
import threading
import os
import sys
import timeit
sys.path.append("../..")
import Teams.ReferenceSolutionAStarCPP.build.astar as AStarCPP
import Framework.Visualizer.maze_visualize


def on_closing():
    """ Callback function if Visualizer Window is closed
    """
    os._exit(0)


apptk = Tk()
apptk.protocol("WM_DELETE_WINDOW", on_closing)
apptk.title("MazeRunner")
apptk.geometry("700x700")
apptk.resizable(True, True)

alg = AStarCPP.AStar("AStar C++")

vis = Framework.Visualizer.maze_visualize.MazeVisualizer(apptk)


def main():
    """[summary]
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'input_file',
        type=str,
        help="The maze as text file"
    )
    args = parser.parse_args()

    if not alg.loadMaze(args.input_file):
        exit(1)

    print(alg.dimRows, alg.dimCols, alg.startRow, alg.startCol, alg.endRow, alg.endCol)

    vis.prepareVisualization(alg.dimRows, alg.dimCols,
                             alg.startRow, alg.startCol, alg.endRow, alg.endCol)
    for row in range(alg.dimRows):
        for col in range(alg.dimCols):
            if alg.getValueAt(row, col) == 1:
                vis.setBlocked(row, col)

    vis.endMaze()

    t = threading.Thread(target=mainloop)
    t.start()
    apptk.mainloop()


def mainloop():
    """[summary]
    """
    starttime = timeit.default_timer()
    alg.solveMaze()
    print("The time difference is :", timeit.default_timer() - starttime)

    for move in alg.came_from:
        if isinstance(move, str):
            a_list = move.split(',')
            map_object = map(int, a_list)
            move = list(map_object)
        vis.addSolutionStep(move[0], move[1])
    vis.plot_route()

    print(
        f'Optimal path needs {len(alg.came_from)}')


if __name__ == "__main__":
    main()
