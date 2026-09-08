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
                    chcp 65001
                    echo Установка зависимостей...
                    C:\\Users\\Егор\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe -m pip install --upgrade pip
                    C:\\Users\\Егор\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe -m pip install -r requirements.txt
                    C:\\Users\\Егор\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe -m pip install pytest uvicorn
                '''
                echo "Зависимости установлены"
            }
        }
        
        stage('Run Tests') {
            steps {
                bat '''
                    chcp 65001
                    echo Запуск тестов...
                    C:\\Users\\Егор\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe -m pytest tests/ -v
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
                    start /B C:\\Users\\Егор\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8080
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