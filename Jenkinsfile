pipeline {
    agent any
    
    environment {
        // Устанавливаем кодировку для правильной работы с русскими символами
        PYTHONIOENCODING = 'UTF-8'
        LANG = 'ru_RU.UTF-8'
    }
    
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
                    chcp 65001
                    echo Создание виртуального окружения...
                    if not exist venv (
                        python -m venv venv --copies
                    )
                    call venv\\Scripts\\activate.bat
                    echo Установка зависимостей...
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                    python -m pip install pytest
                '''
                echo "Окружение настроено"
            }
        }
        
        stage('Run Tests') {
            steps {
                bat '''
                    chcp 65001
                    call venv\\Scripts\\activate.bat
                    echo Запуск тестов...
                    python -m pytest tests/ -v
                '''
                echo "Тесты пройдены"
            }
        }
        
        stage('Deploy') {
            steps {
                echo "Деплой на продакшн..."
                bat '''
                    chcp 65001
                    call venv\\Scripts\\activate.bat
                    echo Запуск сервера...
                    start /B python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
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