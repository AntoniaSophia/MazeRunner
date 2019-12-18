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
Library           BrokerLibrary.py
Library           MazeGuiLibrary.py
Library           GeneratorLibrary.py
Library           AStarSolverLibrary.py
Library           MQTTLibrary

*** Test Cases ***
End2End Maze
    Broker start
    Gui start
    Astar start
    Connect     127.0.0.1
    sleep  1s
    Generator action  11  11  0  0
    sleep  5s
    Publish     topic=/maze    message=solve
    sleep  5s
    Generator action  21  21  0  0
    sleep  5s
    Publish     topic=/maze    message=solve    
    sleep  5s
    Generator action  99  99  0  0
    sleep  10s
    Publish     topic=/maze    message=solve    
    sleep  10s
    Astar stop    
    Gui stop
    Broker stop
