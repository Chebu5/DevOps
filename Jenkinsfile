pipeline {
    agent any

    environment {
        REGISTRY      = 'registry.example.com'
        IMAGE_NAME    = 'my-fastapi-app'
        IMAGE_TAG     = "${env.BUILD_NUMBER}"
        IMAGE_LATEST  = "${REGISTRY}/${IMAGE_NAME}:latest"
        IMAGE_BACKUP  = "${REGISTRY}/${IMAGE_NAME}:backup"
        IMAGE_NEW     = "${REGISTRY}/${IMAGE_NAME}:${env.BUILD_NUMBER}"
        CONTAINER     = 'fastapi-app'
        // Креды для docker login в Jenkins
        REGISTRY_CRED = 'registry-credentials'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Login to registry') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: env.REGISTRY_CRED,
                    usernameVariable: 'REG_USER',
                    passwordVariable: 'REG_PASS'
                )]) {
                    sh '''
                        echo "$REG_PASS" | docker login "$REGISTRY" -u "$REG_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Backup old image in registry') {
            steps {
                sh '''
                    set +e
                    # Пробуем вытащить текущий latest (если он есть в реестре)
                    docker pull "${IMAGE_LATEST}"
                    if [ $? -eq 0 ]; then
                        echo "Old image found. Tagging as backup and pushing..."
                        docker tag  "${IMAGE_LATEST}" "${IMAGE_BACKUP}"
                        docker push "${IMAGE_BACKUP}"
                        echo "Backup saved: ${IMAGE_BACKUP}"
                    else
                        echo "No previous image in registry — first run, skipping backup."
                    fi
                    set -e
                '''
            }
        }

        stage('Build new image') {
            steps {
                sh '''
                    docker build \
                        -t "${IMAGE_NEW}" \
                        -t "${IMAGE_LATEST}" \
                        --label "build=${BUILD_NUMBER}" \
                        --label "commit=${GIT_COMMIT}" \
                        .
                '''
            }
        }

        stage('Push new image') {
            steps {
                sh '''
                    docker push "${IMAGE_NEW}"
                    docker push "${IMAGE_LATEST}"
                '''
            }
        }

        stage('Deploy / Run container') {
            steps {
                sh '''
                    # Останавливаем предыдущий контейнер
                    docker rm -f "${CONTAINER}" 2>/dev/null || true

                    docker run -d \
                        --name "${CONTAINER}" \
                        --restart unless-stopped \
                        -p 8000:8000 \
                        -e PYTHONUNBUFFERED=1 \
                        "${IMAGE_NEW}"
                '''
            }
        }

        stage('Smoke test') {
            steps {
                sh '''
                    for i in $(seq 1 10); do
                        if curl -fsS http://localhost:8000/docs >/dev/null; then
                            echo "App is up"
                            exit 0
                        fi
                        sleep 3
                    done
                    echo "App did not start" >&2
                    docker logs "${CONTAINER}" || true
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo "Deployed ${IMAGE_NEW} (previous saved as ${IMAGE_BACKUP})"
        }
        failure {
            sh '''
                docker logs "${CONTAINER}" 2>/dev/null || true
                docker rm -f "${CONTAINER}" 2>/dev/null || true
            '''
        }
        always {
            sh 'docker image prune -f || true'
        }
    }
}