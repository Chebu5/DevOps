pipeline {
    agent any

    environment {
        DOCKER          = 'C:\\Users\\Eger\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        REGISTRY        = 'localhost:5000'

        APP_NAME        = 'my-fastapi-app'
        NGINX_NAME      = 'my-fastapi-nginx'

        APP_IMAGE       = "${REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER}"
        APP_LATEST      = "${REGISTRY}/${APP_NAME}:latest"

        NGINX_IMAGE     = "${REGISTRY}/${NGINX_NAME}:${env.BUILD_NUMBER}"
        NGINX_LATEST    = "${REGISTRY}/${NGINX_NAME}:latest"

        NETWORK         = 'fastapi-net'
        APP_CONTAINER   = 'fastapi-app'
        NGINX_CONTAINER = 'fastapi-nginx'

        APP_PORT        = '8000'
        NGINX_PORT      = '8081'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }
//if errorlevel 1 "${env.DOCKER}" network create ${env.NETWORK}
        stage('Prepare registry & network') {
            steps {
                bat """
                if not exist "C:\\Users\\Eger\\registry" mkdir "C:\\Users\\Eger\\registry"
                    "${env.DOCKER}" inspect registry >nul 2>nul
                if errorlevel 1 (
                    "${env.DOCKER}" run -d -p 5000:5000 --name registry --restart unless-stopped -v C:\\Users\\Eger\\registry:/var/lib/registry registry:2
                ) else (
                    "${env.DOCKER}" start registry >nul 2>nul
                )

                    "${env.DOCKER}" network inspect ${env.NETWORK} >nul 2>nul

                """
            }
        }

        stage('Build app image') {
            steps {
                bat """
                    "${env.DOCKER}" build -t ${env.APP_IMAGE} -t ${env.APP_LATEST} .
                """
            }
        }

        stage('Build nginx image') {
            steps {
                bat """
                    "${env.DOCKER}" build -f nginx/Dockerfile -t ${env.NGINX_IMAGE} -t ${env.NGINX_LATEST} nginx
                """
            }
        }

        stage('Run & Test') {
            steps {
                bat """
                    "${env.DOCKER}" rm -f ${env.NGINX_CONTAINER} ${env.APP_CONTAINER} 2>nul

                    "${env.DOCKER}" run -d --name ${env.APP_CONTAINER} --network ${env.NETWORK} -p ${env.APP_PORT}:8000 ${env.APP_IMAGE}

                    "${env.DOCKER}" run -d --name ${env.NGINX_CONTAINER} --network ${env.NETWORK} -p ${env.NGINX_PORT}:80 ${env.NGINX_IMAGE}

                    powershell -Command "Start-Sleep -Seconds 5"

                    "${env.DOCKER}" ps
                    curl.exe -f http://localhost:${env.NGINX_PORT}/docs
                """
            }
        }

        stage('Push to local registry') {
            steps {
                bat """
                    "${env.DOCKER}" push ${env.APP_IMAGE}
                    "${env.DOCKER}" push ${env.APP_LATEST}

                    "${env.DOCKER}" push ${env.NGINX_IMAGE}
                    "${env.DOCKER}" push ${env.NGINX_LATEST}
                """
            }
        }

        stage('Show saved images') {
            steps {
                bat """
                    "${env.DOCKER}" images | findstr "${env.APP_NAME}"
                    "${env.DOCKER}" images | findstr "${env.NGINX_NAME}"

                    curl.exe http://localhost:5000/v2/_catalog
                    curl.exe http://localhost:5000/v2/${env.APP_NAME}/tags/list
                    curl.exe http://localhost:5000/v2/${env.NGINX_NAME}/tags/list
                """
            }
        }
    }
}