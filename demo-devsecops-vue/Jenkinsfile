pipeline {
    agent {
        label 'ABN-HW'
    }
    stages {
        stage('SCM from Mirror') {
            steps {
                sh "ls -al"
                sh "pwd"
            }
        }
        stage('Image') {
            steps {
                sh "docker build . -t visualfrontend"
            }
        }
        stage('Start') {
            steps {
                sh 'docker stop visualfrontend | true'
                sh 'docker rm visualfrontend | true'
                sh 'docker run -d --name visualfrontend -p 8190:80 visualfrontend:latest /bin/bash -c "nginx; tail -f /dev/null"'
            }
        }
    }
}
