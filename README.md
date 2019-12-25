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
    ├── ReferenceSolutionBreadthFirst
    ├── TeamB
    ├── TeamC
    ├── TeamD
    ├── TeamE
    └── TeamTemplate
```

# Cathedral and the bazar (www.catb.org/~esr/writings/cathedral-bazaar/)

1. Every good work of software starts by scratching a developer's personal itch.
2. Good programmers know what to write. Great ones know what to rewrite (and reuse).
3. Plan to throw one [version] away; you will, anyhow. (Copied from Frederick Brooks' The Mythical Man-Month)
4. If you have the right attitude, interesting problems will find you.
5. When you lose interest in a program, your last duty to it is to hand it off to a competent successor.
6. Treating your users as co-developers is your least-hassle route to rapid code improvement and effective debugging.
7. Release early. Release often. And listen to your customers.
8. Given a large enough beta-tester and co-developer base, almost every problem will be characterized quickly and the fix obvious to someone.
9. Smart data structures and dumb code works a lot better than the other way around.
10. If you treat your beta-testers as if they're your most valuable resource, they will respond by becoming your most valuable resource.
11. The next best thing to having good ideas is recognizing good ideas from your users. Sometimes the latter is better.
12. Often, the most striking and innovative solutions come from realizing that your concept of the problem was wrong.
13. Perfection (in design) is achieved not when there is nothing more to add, but rather when there is nothing more to take away. (Attributed to Antoine de Saint-Exupéry)
14. Any tool should be useful in the expected way, but a truly great tool lends itself to uses you never expected.
15. When writing gateway software of any kind, take pains to disturb the data stream as little as possible—and never throw away information unless the recipient forces you to!
16. When your language is nowhere near Turing-complete, syntactic sugar can be your friend.
17. A security system is only as secure as its secret. Beware of pseudo-secrets.
18. To solve an interesting problem, start by finding a problem that is interesting to you.
19. Provided the development coordinator has a communications medium at least as good as the Internet, and knows how to lead without coercion, many heads are inevitably better than one.
