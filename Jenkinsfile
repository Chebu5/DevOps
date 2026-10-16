pipeline {
    agent any

    environment {
        DOCKER  = 'C:\\Users\\Eger\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        KUBECTL = 'C:\\Users\\Eger\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\kubectl.exe'
        KUBECONFIG = 'C:\\Users\\Eger\\.kube\\config'

        CATALOG_NAME  = 'my-fastapi-catalog'
        ORDER_NAME    = 'my-fastapi-order'
        NGINX_NAME    = 'my-fastapi-nginx'

        CATALOG_IMAGE = "${CATALOG_NAME}:latest"
        ORDER_IMAGE   = "${ORDER_NAME}:latest"
        NGINX_IMAGE   = "${NGINX_NAME}:latest"

        NETWORK           = 'fastapi-net'
        CATALOG_CONTAINER = 'fastapi-catalog'
        ORDER_CONTAINER   = 'fastapi-order'
        NGINX_CONTAINER   = 'fastapi-nginx'

        CATALOG_PORT = '8001'
        ORDER_PORT   = '8002'
        NGINX_PORT   = '8081'
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

        stage('Build catalog image') {
            steps {
                bat """
                    "${env.DOCKER}" build -t ${env.CATALOG_IMAGE} -f backend-catalog/Dockerfile .
                """
            }
        }

        stage('Build order image') {
            steps {
                bat """
                    "${env.DOCKER}" build -t ${env.ORDER_IMAGE} -f backend-order/Dockerfile .
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
                    "${env.DOCKER}" rm -f ${env.NGINX_CONTAINER} ${env.CATALOG_CONTAINER} ${env.ORDER_CONTAINER} 2>nul

                    "${env.DOCKER}" run -d --name ${env.CATALOG_CONTAINER} --network ${env.NETWORK} -p ${env.CATALOG_PORT}:8000 ${env.CATALOG_IMAGE}
                    "${env.DOCKER}" run -d --name ${env.ORDER_CONTAINER}   --network ${env.NETWORK} -p ${env.ORDER_PORT}:8000 ${env.ORDER_IMAGE}
                    "${env.DOCKER}" run -d --name ${env.NGINX_CONTAINER}   --network ${env.NETWORK} -p ${env.NGINX_PORT}:80 ${env.NGINX_IMAGE}

                    powershell -Command "Start-Sleep -Seconds 5"

                    "${env.DOCKER}" ps
                    curl.exe -f http://localhost:${env.CATALOG_PORT}/health
                    curl.exe -f http://localhost:${env.ORDER_PORT}/health
                """
            }
        }

        stage('Load images into K8s containerd') {
            steps {
                bat """
                    "${env.DOCKER}" save ${env.CATALOG_IMAGE} -o fastapi-catalog.tar
                    "${env.DOCKER}" save ${env.ORDER_IMAGE}   -o fastapi-order.tar
                    "${env.DOCKER}" save ${env.NGINX_IMAGE}   -o fastapi-nginx.tar

                    "${env.DOCKER}" exec -i desktop-control-plane ctr -n k8s.io images import - < fastapi-catalog.tar
                    "${env.DOCKER}" exec -i desktop-control-plane ctr -n k8s.io images import - < fastapi-order.tar
                    "${env.DOCKER}" exec -i desktop-control-plane ctr -n k8s.io images import - < fastapi-nginx.tar

                    del fastapi-catalog.tar fastapi-order.tar fastapi-nginx.tar
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat """
                    "${env.KUBECTL}" apply -f k8s/nginx-configmap.yaml
                    "${env.KUBECTL}" apply -f k8s/static-configmap.yaml

                    "${env.KUBECTL}" apply -f k8s/backend-catalog-deployment.yaml
                    "${env.KUBECTL}" apply -f k8s/backend-catalog-service.yaml
                    "${env.KUBECTL}" apply -f k8s/backend-order-deployment.yaml
                    "${env.KUBECTL}" apply -f k8s/backend-order-service.yaml

                    "${env.KUBECTL}" apply -f k8s/frontend-deployment.yaml
                    "${env.KUBECTL}" apply -f k8s/frontend-service.yaml
                """
            }
        }

        stage('Verify deployment') {
            steps {
                bat """
                    "${env.KUBECTL}" rollout restart deployment/backend-catalog-deployment
                    "${env.KUBECTL}" rollout restart deployment/backend-order-deployment
                    "${env.KUBECTL}" rollout restart deployment/frontend-deployment

                    "${env.KUBECTL}" rollout status deployment/backend-catalog-deployment --timeout=120s
                    "${env.KUBECTL}" rollout status deployment/backend-order-deployment --timeout=120s
                    "${env.KUBECTL}" rollout status deployment/frontend-deployment --timeout=120s

                    "${env.KUBECTL}" get pods
                    "${env.KUBECTL}" get svc
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