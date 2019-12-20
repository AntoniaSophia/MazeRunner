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
Library           BrokerLibrary.py
Library           MazeGuiLibrary.py
Library           GeneratorLibrary.py
Library           AStarSolverLibrary.py
Library           MQTTLibrary
Library           Process
Library           OperatingSystem

*** Test Cases ***
ExecuteUnitTest
    Create Directory  ${CURDIR}/result
    Empty Directory  ${CURDIR}/result
    Run Process  pytest  cwd=${CURDIR}/../Teams/ReferenceSolutionAStar  stdout=${CURDIR}/result/UnitTestResult.txt 

    Run Process  coverage  run  -m  pytest  cwd=${CURDIR}/../Teams
    Run Process  coverage  report  -m  cwd=${CURDIR}/../Teams  stdout=${CURDIR}/result/UnitTestResult.txt
    ${result} =    Get File  ${CURDIR}/result/UnitTestResult.txt
    Log  \n ${result}   console=${True}
    Run Process  coverage  erase
    #Remove Files  ${CURDIR}/result/UnitTestResult.txt
    #Remove Directory  ${CURDIR}/result