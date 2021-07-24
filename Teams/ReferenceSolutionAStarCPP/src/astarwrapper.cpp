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
        generator.setDiagonalMovement(true);
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
        filehandle = std::ifstream(mazepath);        
        while(getline(filehandle,line))
        {
            std::stringstream   linestream(line);
            std::string         value;

            while(getline(linestream,value,','))
            {
                int numval = std::stoi( value );
                if (numval==1){
                    generator.addCollision({xpos, ypos});
                }else if(numval==2){
                    AStar::Vec2i posv({xpos,ypos});
                    startpos=posv;

                }else if(numval==3){
                    AStar::Vec2i posv({xpos,ypos});
                    endpos=posv;
                }
                //std::cout << xpos << "|" << ypos << "Value(" << std::stoi( value ) << ")\n";
                xpos++;
            }
            //std::cout << "Line Finished" << std::endl;
            ypos++;
            xpos=0;
        }
        filehandle.close();
        return true;
    }

    void solveMaze(){
        solpath = generator.findPath(startpos, endpos);
        std::ostringstream stringStream;
        
        std::string copyOfStr = stringStream.str();
        for(auto& coordinate : solpath) {
            stringStream << coordinate.y << "," << coordinate.x;
            copyOfStr = stringStream.str();
            came_from.push_back(copyOfStr);
            stringStream.str(std::string());
        }        
    }

    void setName(const std::string &name_) { name = name_; }
    const std::string &getName() const { return name; }

    std::string name;
    AStar::Generator generator;
    AStar::Vec2i startpos;
    AStar::Vec2i endpos;
    AStar::CoordinateList solpath;
    std::vector<std::string> came_from;
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
        .def_readwrite("came_from", &AStarWrapper::came_from);
}