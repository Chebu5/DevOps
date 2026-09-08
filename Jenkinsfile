pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Код получен из ветки: ${env.BRANCH_NAME}"
            }
        }
        
        stage('Setup') {
            steps {
                bat '''
                    echo Создание виртуального окружения...
                    if not exist venv (
                        python -m venv venv
                    )
                    call venv\\Scripts\\activate.bat
                    echo Установка зависимостей...
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
                '''
                echo "Окружение настроено"
            }
        }
        
        stage('Run Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    echo Запуск тестов...
                    pytest tests/ -v
                '''
                echo "Тесты пройдены"
            }
        }
        
        stage('Deploy') {
            steps {
                echo "Деплой на продакшн..."
                bat '''
                    call venv\\Scripts\\activate.bat
                    echo Запуск сервера...
                    start /B uvicorn app.main:app --host 0.0.0.0 --port 8080
                '''
                echo "Сервер запущен на http://localhost:8080"
            }
        }
    }
    
    post {
        success {
            echo "Pipeline выполнен успешно!"
        }
        failure {
            echo "Pipeline завершился с ошибкой!"
        }
    }
}