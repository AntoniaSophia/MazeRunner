#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "source/AStar.hpp"
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include<algorithm>
#include<iterator>

namespace py = pybind11;
using namespace std;

struct AStarWrapper {
    AStarWrapper(const std::string &name) : name(name) { 
        generator.setHeuristic(AStar::Heuristic::euclidean);
        generator.setDiagonalMovement(false);
    }


    bool loadMaze(std::string &mazepath){
        int ypos=0;
        int xpos=0;
        std::ifstream filehandle(mazepath);
        int number_of_lines = 0;
        std::string line;
        int length=0;
        while (std::getline(filehandle, line)){
            ++number_of_lines;
            length=1+(line.length()-1)/2;

        }

        cout << number_of_lines << "|" << length << endl;
        filehandle.close();

        generator.setWorldSize({length,number_of_lines});

        ary = new int[number_of_lines*length];

        filehandle = std::ifstream(mazepath);        
        while(getline(filehandle,line))
        {
            std::stringstream   linestream(line);
            std::string         value;

            while(getline(linestream,value,','))
            {
                int numval = std::stoi( value );
                ary[ypos*length+xpos]=numval;

                if (numval==1){
                    generator.addCollision({xpos,ypos});
                }else if(numval==2){
                    AStar::Vec2i posv({xpos,ypos});
                    startpos=posv;
                    startRow=ypos;
                    startCol=xpos;

                }else if(numval==3){
                    AStar::Vec2i posv({xpos,ypos});
                    endpos=posv;
                    endRow=ypos;
                    endCol=xpos;

                }
                //std::cout << xpos << "|" << ypos << "Value(" << std::stoi( value ) << ")\n";
                xpos++;
            }
            //std::cout << "Line Finished" << std::endl;
            ypos++;
            xpos=0;
        }
        filehandle.close();
        dimCols=length;
        dimRows=number_of_lines;
        return true;
    }

    void solveMaze(){
        solpath = generator.findPath(startpos, endpos);
        std::ostringstream stringStream;

        std::string copyOfStr = stringStream.str();

        for (auto &coordinate : solpath)
        {
            stringStream << coordinate.y<< "," << coordinate.x;
            copyOfStr = stringStream.str();
            came_from.insert(came_from.begin(), copyOfStr);
            stringStream.str(std::string());
        }
    }
    
    int getValueAt(int ypos, int xpos) { return ary[ypos*dimCols+xpos];}

    void setName(const std::string &name_) { name = name_; }
    const std::string &getName() const { return name; }

    std::string name;
    AStar::Generator generator;
    AStar::Vec2i startpos;
    AStar::Vec2i endpos;
    AStar::CoordinateList solpath;
    std::vector<std::string> came_from;
    int dimRows;
    int dimCols;
    int startRow;
    int startCol;
    int endRow;
    int endCol;    
    int *ary;

};

PYBIND11_MODULE(astar, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: cmake_example

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";
    m.attr("__version__") = "dev";
    py::class_<AStarWrapper>(m, "AStar")
        .def(py::init<const std::string &>())
        .def("setName", &AStarWrapper::setName)
        .def("getName", &AStarWrapper::getName)
        .def("loadMaze", &AStarWrapper::loadMaze)
        .def("solveMaze", &AStarWrapper::solveMaze)
        .def("getValueAt", &AStarWrapper::getValueAt)        
        .def_readwrite("came_from", &AStarWrapper::came_from)
        .def_readwrite("dimRows", &AStarWrapper::dimRows)
        .def_readwrite("dimCols", &AStarWrapper::dimCols)
        .def_readwrite("startRow", &AStarWrapper::startRow)
        .def_readwrite("startCol", &AStarWrapper::startCol)
        .def_readwrite("endRow", &AStarWrapper::endRow)
        .def_readwrite("endCol", &AStarWrapper::endCol);


}