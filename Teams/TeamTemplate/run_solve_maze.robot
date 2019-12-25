*** Settings ***
Documentation     Example test cases using a keyword-driven testing approach.
...
Library           ../../robotframework/Framework/BrokerLibrary.py
Library           ../../robotframework/Framework/MazeGuiLibrary.py
Library           ../../robotframework/Framework/GeneratorLibrary.py
Library           TeamTemplateAlgoRobotLibrary.py
Library           MQTTLibrary
Library           Process
Library           OperatingSystem

*** Test Cases ***
#Start command: robot <robotfile> , 
#               example: robot -d _tmp_robot_reports run_all.robot
RobotScriptSolveMaze
    TeamTemplateAlgo start
    sleep  2s
    TeamTemplateAlgo stop
