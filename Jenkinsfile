pipeline {
    agent any
    
    stages {
        stage('Получение кода') {
            steps {
                checkout scm
                echo "Код получен. Ветка: ${env.GIT_BRANCH}"
            }
        }

        stage('Установка зависимостей') {
            when {
                expression { env.GIT_BRANCH == 'main' }
            }
            steps {
                bat '''
                    echo "Создание venv и установка зависимостей..."
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Запуск тестов') {
            when {
                expression { env.GIT_BRANCH == 'main' }
            }
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    python -m pytest tests/ -v
                '''
            }
        }
        
        stage('Деплой') {
            when {
                expression { env.GIT_BRANCH == 'main' }
            }
            steps {
                bat '''
                    echo "Запуск сервера..."
                    call venv\\Scripts\\activate.bat
                    start /B python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
                    echo "Сервер запущен на http://localhost:8000"
                '''
            }
        }
        
        stage('Инфо') {
            when {
                not { branch 'main' }
            }
            steps {
                echo "Деплой только для main. Текущая ветка: ${env.GIT_BRANCH}"
            }
        }
    }
    
    post {
        success {
            echo "Готово! Ветка: ${env.GIT_BRANCH}"
        }
        failure {
            echo "Ошибка! Ветка: ${env.GIT_BRANCH}"
        }
    }
}