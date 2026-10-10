pipeline {
    agent any

    environment {
        DOCKER  = 'C:\\Users\\Eger\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        KUBECTL = 'C:\\Users\\Eger\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\kubectl.exe'
        KUBECONFIG = 'C:\\Users\\Eger\\.kube\\config'
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
        stage('Load images into K8s containerd') {
            steps {
                bat """
                    "${env.DOCKER}" save ${env.APP_IMAGE} -o fastapi-app.tar
                    "${env.DOCKER}" save ${env.NGINX_IMAGE} -o fastapi-nginx.tar

                    "${env.DOCKER}" exec -i desktop-control-plane ctr -n k8s.io images import - < fastapi-app.tar
                    "${env.DOCKER}" exec -i desktop-control-plane ctr -n k8s.io images import - < fastapi-nginx.tar

                    del fastapi-app.tar fastapi-nginx.tar
                """
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                bat """
                    "${env.KUBECTL}" apply -f k8s/db-pvc.yaml
                    "${env.KUBECTL}" apply -f k8s/nginx-configmap.yaml
                    "${env.KUBECTL}" apply -f k8s/static-configmap.yaml
                    "${env.KUBECTL}" apply -f k8s/backend-deployment.yaml
                    "${env.KUBECTL}" apply -f k8s/backend-service.yaml
                    "${env.KUBECTL}" apply -f k8s/frontend-deployment.yaml
                    "${env.KUBECTL}" apply -f k8s/frontend-service.yaml
                """
            }
        }

        stage('Verify deployment') {
            steps {
                bat """
                    "${env.KUBECTL}" rollout status deployment/backend-deployment --timeout=120s
                    "${env.KUBECTL}" rollout status deployment/frontend-deployment --timeout=120s

                    "${env.KUBECTL}" get pods
                    "${env.KUBECTL}" get svc
                    "${env.KUBECTL}" get pvc
                """
            }
        }

        stage('Smoke test (K8s)') {
            steps {
                bat """
                    powershell -Command "Start-Sleep -Seconds 15"
                    curl.exe -f http://localhost:30080/api/health
                """
            }
        }
    }

    post {
        always {
            bat """
                "${env.DOCKER}" ps -a || exit /b 0
                "${env.KUBECTL}" get pods -o wide || exit /b 0
                "${env.KUBECTL}" get events --sort-by=.lastTimestamp || exit /b 0
            """
        }
    }
}