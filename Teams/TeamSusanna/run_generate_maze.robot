*** Settings ***
Documentation     Example test cases using a keyword-driven testing approach.
...
Library           ../../robotframework/Framework/BrokerLibrary.py
Library           ../../robotframework/Framework/MazeGuiLibrary.py
Library           ../../robotframework/Framework/GeneratorLibrary.py
Library           TeamTemplateClientRobotLibrary.py
Library           MQTTLibrary
Library           Process
Library           OperatingSystem

*** Test Cases ***
#Start command: robot <robotfile> , 
#               example: robot -d _tmp_robot_reports run_all.robot
RobotScriptGenerateMaze
    Broker start
    #Gui start
    TeamTemplateClient start
    Connect     127.0.0.1
    sleep  2s
    #Generator action  5  5  0  0
    Generator load  ../../MazeExamples/maze1.txt

    TeamTemplateClient stop
    Broker stop
