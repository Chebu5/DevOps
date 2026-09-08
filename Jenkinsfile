pipeline {
    agent any
    
    stages {
        stage('📥 Получение кода из GitHub') {
            steps {
                checkout scm
                echo "✅ Код получен из репозитория"
                echo "✅ Ветка: ${env.BRANCH_NAME}"
            }
        }
        
        stage('🔧 Установка зависимостей') {
            steps {
                bat '''
                    echo "Установка зависимостей..."
                    if not exist venv (
                        python -m venv venv
                    )
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install uvicorn
                    echo "✅ Окружение готово"
                '''
            }
        }
        
        stage('🚀 Доставка и деплой (CD)') {
            when {
                branch 'main'
            }
            steps {
                echo """
                ========================================
                ЗАПУСК CD ПРОЦЕССА
                Ветка: main
                ========================================
                """
                bat '''
                    call venv\\Scripts\\activate.bat
                    echo "Запуск приложения на порту 8080..."
                    start /B python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
                    echo "✅ Приложение успешно развернуто!"
                    echo "🌐 Доступно по адресу: http://localhost:8080"
                '''
            }
        }
        
        stage('ℹ️ Информация о ветке') {
            when {
                not { branch 'main' }
            }
            steps {
                echo """
                ════════════════════════════════════════════════
                📌 ВЕТКА: ${env.BRANCH_NAME}
                ℹ️  CD процесс пропущен (активен только для main)
                📌 Для деплоя сделайте merge в main
                ════════════════════════════════════════════════
                """
            }
        }
    }
    
    post {
        success {
            echo """
            ════════════════════════════════════════════════
            ✅ ПАЙПЛАЙН ВЫПОЛНЕН УСПЕШНО!
            📌 Ветка: ${env.BRANCH_NAME}
            🚀 CD: ${env.BRANCH_NAME == 'main' ? '✅ Выполнен' : '⏭️ Пропущен (не main)'}
            ════════════════════════════════════════════════
            """
        }
        failure {
            echo """
            ════════════════════════════════════════════════
            ❌ ПАЙПЛАЙН ЗАВЕРШИЛСЯ С ОШИБКОЙ!
            📌 Ветка: ${env.BRANCH_NAME}
            🔍 Проверьте логи выше для исправления
            ════════════════════════════════════════════════
            """
        }
    }
}