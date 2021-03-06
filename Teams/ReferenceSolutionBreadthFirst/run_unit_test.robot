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
Library           Process
Library           OperatingSystem

*** Test Cases ***
ExecuteUnitTest
    #Start command: robot -d _tmp_robot_reports <robotfile> , e.g. robot -d _tmp_robot_reports run_unit_test.robot
    Create Directory  ${CURDIR}/_tmp_unit_test_result
    Empty Directory  ${CURDIR}/_tmp_unit_test_result

    ${result} =    RunProcess  pytest  cwd=${CURDIR}/tests  stderr=STDOUT  stdout=${CURDIR}/_tmp_unit_test_result/UnitTestResult.txt 
    ${logtext} =    Get File  ${CURDIR}/_tmp_unit_test_result/UnitTestResult.txt
    
    Run keyword if   ${result.rc} is not 0   Log  \n ${logtext}   console=${True}    
    Run keyword if   ${result.rc} is not 0   Fatal Error     \nPytest exist with error! Please check the unittest!\n

    Run Process  coverage  run  -m  pytest  cwd=${CURDIR}/tests  env:COVERAGE_FILE=${CURDIR}/tests/.coverage
    Run Process  coverage  report  -m  cwd=${CURDIR}/tests  env:COVERAGE_FILE=${CURDIR}/tests/.coverage  stdout=${CURDIR}/_tmp_unit_test_result/CoverageUnitTestResult.txt
    ${result} =    Get File  ${CURDIR}/_tmp_unit_test_result/CoverageUnitTestResult.txt
    Log  \n ${result}   console=${True}

    Remove Files  ${CURDIR}/tests/.coverage
