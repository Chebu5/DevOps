pipeline {
    agent any

    environment {
        DOCKER     = 'C:\\Users\\Eger\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        IMAGE_NAME = 'my-fastapi-app'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        IMAGE      = "${env.IMAGE_NAME}:${env.BUILD_NUMBER}"
        CONTAINER  = 'fastapi-app'
        APP_PORT   = '8000'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Docker info') {
            steps {
                bat "\"${env.DOCKER}\" version"
                bat "\"${env.DOCKER}\" info"
            }
        }

        stage('Build image') {
            steps {
                bat "\"${env.DOCKER}\" build -t ${env.IMAGE} -t ${env.IMAGE_NAME}:latest ."
            }
        }

        stage('Run container') {
            steps {
                bat """
                    "${env.DOCKER}" rm -f ${env.CONTAINER} 2>nul
                    "${env.DOCKER}" run -d --name ${env.CONTAINER} -p ${env.APP_PORT}:8000 -e PYTHONUNBUFFERED=1 ${env.IMAGE}
                """
            }
        }

        stage('Smoke test') {
            steps {
                bat """
                    setlocal enabledelayedexpansion
                    set OK=0
                    for /L %%i in (1,1,10) do (
                        curl -fsS http://localhost:${env.APP_PORT}/docs >nul 2>&1
                        if !errorlevel! equ 0 (
                            echo App is up
                            set OK=1
                            goto :done
                        )
                        timeout /t 3 /nobreak >nul
                    )
                    :done
                    if "!OK!"=="0" (
                        echo App did not start
                        "${env.DOCKER}" logs ${env.CONTAINER}
                        exit /b 1
                    )
                """
            }
        }
    }

    post {
        failure {
            bat """
                "${env.DOCKER}" logs ${env.CONTAINER} 2>nul
                "${env.DOCKER}" rm -f ${env.CONTAINER} 2>nul
                exit /b 0
            """
        }
    }
}