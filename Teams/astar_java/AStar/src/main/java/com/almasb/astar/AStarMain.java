package com.almasb.astar;


public class AStarMain {

    private static final int GRID_SIZE = 20;
    private AStarGrid grid;

    public AStarMain() {
        this.grid = new AStarGrid(GRID_SIZE, GRID_SIZE);
    }
    
    public static void main(String[] args) {
        // Prints "Hello, World" to the terminal window.

        AStarMain astarmain = new AStarMain();

        System.out.println("Hello, World");
    }

}
