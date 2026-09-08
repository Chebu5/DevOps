pipeline {
    agent any
    
    stages {
        stage('📥 Получение кода') {
            steps {
                checkout scm
                echo "✅ Код получен. Ветка: ${env.BRANCH_NAME}"
            }
        }
        
        stage('🚀 Деплой') {
            when {
                branch 'main'
            }
            steps {
                bat '''
                    echo "Запуск сервера..."
                    start /B python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
                    echo "✅ Сервер запущен на http://localhost:8080"
                '''
            }
        }
        
        stage('ℹ️ Инфо') {
            when {
                not { branch 'main' }
            }
            steps {
                echo "Деплой только для main. Текущая ветка: ${env.BRANCH_NAME}"
            }
        }
    }
    
    post {
        success {
            echo "✅ Готово! Ветка: ${env.BRANCH_NAME}"
        }
        failure {
            echo "❌ Ошибка! Ветка: ${env.BRANCH_NAME}"
        }
    }
}
