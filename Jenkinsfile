pipeline {
    agent any

    environment {
        REGISTRY      = 'registry.example.com'
        IMAGE_NAME    = 'my-fastapi-app'
        IMAGE_LATEST  = "${REGISTRY}/${IMAGE_NAME}:latest"
        IMAGE_BACKUP  = "${REGISTRY}/${IMAGE_NAME}:backup"
        IMAGE_NEW     = "${REGISTRY}/${IMAGE_NAME}:${env.BUILD_NUMBER}"
        CONTAINER     = 'fastapi-app'
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
                    bat """
                        echo %REG_PASS% | docker login ${REGISTRY} -u %REG_USER% --password-stdin
                    """
                }
            }
        }

        stage('Backup old image in registry') {
            steps {
                bat """
                    docker pull ${IMAGE_LATEST}
                    if errorlevel 1 (
                        echo No previous image in registry - first run, skipping backup.
                    ) else (
                        docker tag ${IMAGE_LATEST} ${IMAGE_BACKUP}
                        docker push ${IMAGE_BACKUP}
                        echo Backup saved: ${IMAGE_BACKUP}
                    )
                """
            }
        }

        stage('Build new image') {
            steps {
                bat """
                    docker build -t ${IMAGE_NEW} -t ${IMAGE_LATEST} --label build=%BUILD_NUMBER% --label commit=%GIT_COMMIT% .
                """
            }
        }

        stage('Push new image') {
            steps {
                bat """
                    docker push ${IMAGE_NEW}
                    docker push ${IMAGE_LATEST}
                """
            }
        }

        stage('Deploy / Run container') {
            steps {
                bat """
                    docker rm -f ${CONTAINER} 2>nul
                    docker run -d --name ${CONTAINER} --restart unless-stopped -p 8000:8000 -e PYTHONUNBUFFERED=1 ${IMAGE_NEW}
                """
            }
        }

        stage('Smoke test') {
            steps {
                bat """
                    for /L %%i in (1,1,10) do (
                        curl -fsS http://localhost:8000/docs >nul 2>&1 && (
                            echo App is up
                            goto :ok
                        )
                        timeout /t 3 /nobreak >nul
                    )
                    echo App did not start
                    docker logs ${CONTAINER}
                    exit /b 1
                    :ok
                """
            }
        }
    }

    post {
        success {
            echo "Deployed ${env.IMAGE_NEW} (previous saved as ${env.IMAGE_BACKUP})"
        }
        failure {
            bat """
                docker logs ${CONTAINER} 2>nul
                docker rm -f ${CONTAINER} 2>nul
                exit /b 0
            """
        }
        always {
            bat "docker image prune -f || exit /b 0"
        }
    }
}