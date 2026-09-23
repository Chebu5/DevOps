pipeline {
    agent any

    environment {
        DOCKER    = 'C:\\Users\\Eger\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        IMAGE     = "my-fastapi-app:${env.BUILD_NUMBER}"
        CONTAINER = 'fastapi-app'
        PORT      = '8000'
    }

    stages {

        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build') {
            steps {
                bat "\"${env.DOCKER}\" build -t ${env.IMAGE} -t my-fastapi-app:latest ."
            }
        }

        stage('Run & Test') {
            steps {
                bat """
                    "${env.DOCKER}" rm -f ${env.CONTAINER} 2>nul
                    "${env.DOCKER}" run -d --name ${env.CONTAINER} -p ${env.PORT}:8000 ${env.IMAGE}
                    powershell -Command "Start-Sleep -Seconds 5"
                    "${env.DOCKER}" ps
                    curl -f http://localhost:${env.PORT}/docs
                """
            }
        }
    }
}