pipeline {
    agent any

    environment {
        DOCKER = 'C:\\Users\\Eger\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'

        APP_NAME   = 'my-fastapi-app'
        NGINX_NAME = 'my-fastapi-nginx'

        APP_IMAGE   = "${APP_NAME}:latest"
        NGINX_IMAGE = "${NGINX_NAME}:latest"

        NETWORK         = 'fastapi-net'
        APP_CONTAINER   = 'fastapi-app'
        NGINX_CONTAINER = 'fastapi-nginx'

        APP_PORT   = '8000'
        NGINX_PORT = '8081'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare network') {
            steps {
                bat """
                    "${env.DOCKER}" network inspect ${env.NETWORK} >nul 2>nul
                    if errorlevel 1 "${env.DOCKER}" network create ${env.NETWORK}
                """
            }
        }

        stage('Build app image') {
            steps {
                bat """
                    "${env.DOCKER}" build -t ${env.APP_IMAGE} ./backend
                """
            }
        }

        stage('Build nginx image') {
            steps {
                bat """
                    "${env.DOCKER}" build -f frontend/nginx/Dockerfile -t ${env.NGINX_IMAGE} frontend
                """
            }
        }

        stage('Run & Test (Docker)') {
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

        stage('Deploy to Kubernetes') {
            steps {
                bat """
                    kubectl apply -f k8s/db-pvc.yaml
                    kubectl apply -f k8s/nginx-configmap.yaml
                    kubectl apply -f k8s/static-configmap.yaml
                    kubectl apply -f k8s/backend-deployment.yaml
                    kubectl apply -f k8s/backend-service.yaml
                    kubectl apply -f k8s/frontend-deployment.yaml
                    kubectl apply -f k8s/frontend-service.yaml
                """
            }
        }

        stage('Verify deployment') {
            steps {
                bat """
                    kubectl rollout status deployment/backend-deployment --timeout=120s
                    kubectl rollout status deployment/frontend-deployment --timeout=120s

                    kubectl get pods
                    kubectl get svc
                    kubectl get pvc
                """
            }
        }

        stage('Smoke test (K8s)') {
            steps {
                bat """
                    powershell -Command "Start-Sleep -Seconds 10"
                    curl.exe -f http://localhost:30080/health
                    curl.exe -f http://localhost:30080/docs
                """
            }
        }
    }

    post {
        always {
            bat """
                "${env.DOCKER}" ps -a || exit /b 0
                kubectl get pods -o wide || exit /b 0
                kubectl get events --sort-by=.lastTimestamp || exit /b 0
            """
        }
    }
}