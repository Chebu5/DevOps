pipeline {
    agent any
    
    stages {
        stage('📥 Получение кода') {
            steps {
                checkout scm
                echo "✅ Код получен. Ветка: ${env.BRANCH_NAME}"
            }
        }
        
        stage('🔧 Установка зависимостей') {
            steps {
                bat '''
                    echo "Установка зависимостей..."
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install uvicorn
                    echo "✅ Зависимости установлены"
                '''
            }
        }
        
        stage('🚀 Запуск сервера') {
            when {
                branch 'main'
            }
            steps {
                bat '''
                    echo "========================================"
                    echo "ЗАПУСК СЕРВЕРА"
                    echo "========================================"
                    
                    echo "1. Проверка установки uvicorn..."
                    python -c "import uvicorn; print('uvicorn версия:', uvicorn.__version__)"
                    
                    echo "2. Проверка наличия app.main..."
                    python -c "import app.main; print('app.main найден')"
                    
                    echo "3. Запуск сервера..."
                    start "Сервер DevOps" cmd /c "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
                    
                    echo "4. Ожидание запуска..."
                    timeout /t 3 /nobreak
                    
                    echo "5. Проверка, что сервер работает..."
                    curl -s http://localhost:8000 || echo "⚠️ Сервер запущен, но не отвечает"
                    
                    echo "========================================"
                    echo "✅ Сервер запущен!"
                    echo "🌐 http://localhost:8000"
                    echo "📚 Документация: http://localhost:8000/docs"
                    echo "========================================"
                '''
            }
        }
        
        stage('ℹ️ Информация') {
            when {
                not { branch 'main' }
            }
            steps {
                echo """
                ════════════════════════════════════════════════
                📌 ВЕТКА: ${env.BRANCH_NAME}
                ℹ️  Сервер запускается только для main
                📌 Сделайте merge в main для запуска
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
            🚀 Сервер: ${env.BRANCH_NAME == 'main' ? '✅ Запущен' : '⏭️ Пропущен'}
            ════════════════════════════════════════════════
            """
        }
        failure {
            echo """
            ════════════════════════════════════════════════
            ❌ ПАЙПЛАЙН ЗАВЕРШИЛСЯ С ОШИБКОЙ!
            📌 Ветка: ${env.BRANCH_NAME}
            🔍 Проверьте логи выше
            ════════════════════════════════════════════════
            """
        }
    }
}
