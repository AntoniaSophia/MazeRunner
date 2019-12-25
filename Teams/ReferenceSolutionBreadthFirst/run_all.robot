*** Settings ***
Documentation     Example test cases using the keyword-driven testing approach.
...
...               All tests contain a workflow constructed from keywords in
...               ``CalculatorLibrary.py``. Creating new tests or editing
...               existing is easy even for people without programming skills.
...
...               The _keyword-driven_ appoach works well for normal test
...               automation, but the _gherkin_ style might be even better
...               if also business people need to understand tests. If the
...               same workflow needs to repeated multiple times, it is best
...               to use to the _data-driven_ approach.
...     	      Start command: robot <robotfile> , e.g. robot keyword_driven.robot
...               dtrhreth
Library           ../../robotframework/Framework/BrokerLibrary.py
Library           ../../robotframework/Framework/MazeGuiLibrary.py
Library           ../../robotframework/Framework/GeneratorLibrary.py
Library           ../../robotframework/Teams/ReferenceSolutionBreadthFirst/BreadthFirstReferenceSolverLibrary.py
Library           MQTTLibrary
Library           Process
Library           OperatingSystem

*** Test Cases ***
#Start command: robot <robotfile> , 
#               example: robot -d _tmp_robot_reports run_all.robot
RunMaze
    Broker start
    Gui start
    BreadthFirstReference start
    Connect     127.0.0.1
    sleep  2s
    #Generator action  11  11  0  0
    Generator load  ../../MazeExamples/maze1.txt
    sleep  5s
    Publish     topic=/maze    message=solve
    sleep  200s
