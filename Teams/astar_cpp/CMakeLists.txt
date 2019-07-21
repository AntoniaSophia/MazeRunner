cmake_minimum_required(VERSION 2.8.9)
project (AStarCPP)

find_package(Boost 1.67.0 COMPONENTS graph)

if(Boost_FOUND)
  include_directories(${Boost_INCLUDE_DIRS})
endif()

add_executable(astar_cpp Astar-Maze-Solver/astar_maze.cpp)

set(PAHO_CPP_LIB paho-mqttpp3 paho-mqtt3c 
                 paho-mqtt3as paho-mqtt3a)

add_subdirectory(samples)

