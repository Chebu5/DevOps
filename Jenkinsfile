pipeline {
    agent any
    
    environment {
        // Ваш путь к Python
        PYTHON_PATH = 'C:\\Users\\Егор\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe'
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
                    echo Установка зависимостей...
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                    venv\\Scripts\\python.exe -m pip install pytest uvicorn
                '''
                echo "Окружение настроено"
            }
        }
        
        stage('Run Tests') {
            steps {
                bat '''
                    chcp 65001
                    echo Запуск тестов...
                    venv\\Scripts\\python.exe -m pytest tests/ -v
                '''
                echo "Тесты пройдены"
            }
        }
        
        stage('Deploy') {
            steps {
                echo "Деплой на продакшн..."
                bat '''
                    chcp 65001
                    echo Запуск сервера...
                    start /B venv\\Scripts\\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8080
                '''
                echo "Сервер запущен на http://localhost:8080"
            }
        }
    }
    
    post {
        success {
            echo "✅ Pipeline выполнен успешно!"
        }
        failure {
            echo "❌ Pipeline завершился с ошибкой!"
        }
    }
}