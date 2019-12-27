# MazeRunner

## Install for Windows 10
1. Python3.7
download and install the latest Installer for 3.7.x Version from https://www.python.org/ftp/python/
e.g. https://www.python.org/ftp/python/3.7.6/python-3.7.6-amd64.exe
2. Git-Client
download and install the git client for windows from https://git-scm.com/download/win
e.g. https://github.com/git-for-windows/git/releases/download/v2.24.1.windows.2/Git-2.24.1.2-64-bit.exe
3. clone this repository ```git clone https://github.com/AntoniaSophia/MazeRunner.git```
2. Open Commandline via ```<win>+r cmd```
3. cd into cloned directory
3. Update pip ```pip install --upgrade pip```
4. Install required python packages: ```pip install -U -r requirements.txt```

## Visual Studio Code 
1. Download and install Visual Studio Code from https://code.visualstudio.com/Download#
2. Install Python Extension: https://marketplace.visualstudio.com/items?itemName=ms-python.python
3. Install Robot Testframework extension https://marketplace.visualstudio.com/items?temName=vivainio.robotframework

## Execute unittests
```pytest -v```

## Execute Robotframework Tests
```cd robotframework
robot end2end_astar.robot
```

## Maze Runner in python with MQTT
This project is for educational purpose. Mazerunner is a collection of applications to introduce Service orientation, IoT Technologies and collaborative Development using state of the art DevOps systems like github and jenkins. 

**DevOps** is a set of software development practices that combine software development (Dev) and information technology operations (Ops) to shorten the systems development life cycle while delivering features, fixes, and updates frequently in close alignment with business objectives.

**MQTT** stands for Message Queuing Telemetry Transport. It is a lightweight publish and subscribe system where you can publish and receive messages as a client. For almost every language and devcies, libraries are available to implement Publisher and Subscriber communicating in heterogenes networks e.g. https://www.mysensors.org/build/mqtt_gateway


![maze](doc/3D-monster-maze.png "maze")
## Maze Application 
```bash
├── docker
│   ├── Dockerfile      A script to create a image to build and run c++ and java applications
│   └── Makefile        Definition how to build the image or other applications, used by make-tool 
├── Framework           
│   ├── Control         Gui application to call other applications
│   ├── DotMatrix       Used for the IoT Demonstration 
│   ├── Generator       Maze generator application
│   ├── Interface       Interface definitions of the mazerunner project
│   ├── MQTTBroker      MQTT tools and broker for windows from Mosquitto project
│   ├── README.md
│   ├── Test            Tests for the mazerunner project
│   └── Visualizer      Gui application to visualize the Maze for Generator and for solver
├── install.bat
├── jenkins             Used for CI Demonstration
├── Jenkinsfile         Build and deployment pipeline for Mazerunner in Jenkins
├── README.md
├── requirements.txt    Python module dependencies of Mazerunner used with "pip install -r requirements.txt."
└── Teams
    ├── README.md
    ├── ReferenceSolutionAStar 
    ├── ReferenceSolutionBreadthFirst#
    ├── TeamA
    ├── TeamB
    ├── TeamC
    ├── TeamD
    ├── TeamE
    └── TeamTemplate
```