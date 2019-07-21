package com.almasb.astar.maze;
import com.almasb.astar.AStarGrid;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public class MazeMain {

    private static final int GRID_SIZE = 20;
    private Maze maze;

    public MazeMain() {
        this.maze = new Maze(GRID_SIZE, GRID_SIZE);
    }
    
    public List<MazeCell> getPath(int startX, int startY, int targetX, int targetY){
        return this.maze.getPath(startX,startY,targetX,targetY);
    }

    public static void main(String[] args) {
        // Prints "Hello, World" to the terminal window.

        MazeMain mazemain = new MazeMain();
        
        System.out.println(mazemain.getPath(1,1,18,18));

        System.out.println("Hello, World");
    }

}
