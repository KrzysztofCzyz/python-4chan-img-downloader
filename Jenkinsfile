pipeline{
    agent none
    options {
        skipStagesAfterUnstable()
    }
    stages{
        stage('Build') {
            agent {
                docker {
                    image 'python:3-alpine'
                }
            }
            steps {
                sh 'python src/setup.py build'
            }
        }
        stage('Test') {
            agent {
                docker{
                    image 'img-downloader-test:v0.01'
                }
            }
            steps {
                sh 'cd src && tox'
            }
            post {
                always {
                    junit ' test.xml'
                }
            }
        }
    }
}