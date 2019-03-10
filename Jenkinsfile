pipeline {
    agent {
        label {
            label ""
            customWorkspace "D:\\_Projects\\MazeRunner\\jenkins_build\\${BRANCH_NAME}"
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
                dir (testWorkspace + "\\Framework\\Test") {
                    sh(script: "python broker_test.py" , returnStdout: true)
                }
            }
        }
    }
}