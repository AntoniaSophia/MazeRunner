pipeline {
    agent any 
    stages {
        stage('Stage SayHello') {
            steps {
                echo 'Hello Mazerunner!' 
            }
        }

        stage('Stage Setup') {
            steps {
                dir ('build_home') {
                  D:\_Projects\MazeRunner\jenkins_build
                }
            }
        }
    }
}