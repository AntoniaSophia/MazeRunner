pipeline {
    agent {
        label {
            label ""
            customWorkspace "D:\\_Projects\\MazeRunner\\jenkins_build\\${BRANCH_NAME}"
            testWorkspace "D:\\_Projects\\MazeRunner\\jenkins_build\\${BRANCH_NAME}\\Framework\\Test"
        }
    }

    stages {
        stage('Stage SayHello') {
            steps {
                echo 'Hello Mazerunner!' 
            }
        }

        stage('Stage Setup') {
            steps {
                echo 'Hello Setup'
                dir (testWorkspace) {
                    sh(script: "python broker_test.py" , returnStdout: true)
                }
            }
        }
    }
}