pipeline {
    agent any

    environment {
        BRANCH = env.BRANCH_NAME
        APP_PORT = '8080'
    }

    stages {

        // ========== 1. СВЯЗЬ С GITHUB ==========
        stage('📥 Получение кода из GitHub') {
            steps {
                checkout scm
                echo """
                ✅ Репозиторий: ${env.GIT_URL}
                ✅ Ветка: ${BRANCH}
                ✅ Коммит: ${env.GIT_COMMIT}
                ✅ Автор: ${env.GIT_AUTHOR_NAME}
                """
            }
        }

        // ========== 2. НАСТРОЙКА ОКРУЖЕНИЯ ==========
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

        // ========== 3. ДОСТАВКА (CD) ТОЛЬКО ДЛЯ MAIN ==========
        stage('🚀 Доставка и деплой (CD)') {
            when {
                branch 'main'
            }
            steps {
                bat '''
                    echo "========================================"
                    echo "ЗАПУСК CD ПРОЦЕССА"
                    echo "Ветка: ${BRANCH}"
                    echo "========================================"
                    call venv\\Scripts\\activate.bat
                    echo "Запуск приложения на порту ${APP_PORT}..."
                    start /B python -m uvicorn app.main:app --host 127.0.0.1 --port ${APP_PORT}
                    echo "✅ Приложение успешно развернуто!"
                    echo "🌐 Доступно по адресу: http://localhost:${APP_PORT}"
                '''
            }
        }

        // ========== 4. ИНФОРМАЦИЯ ДЛЯ ДРУГИХ ВЕТОК ==========
        stage('ℹ️ Информация о ветке') {
            when {
                not { branch 'main' }
            }
            steps {
                echo """
                ════════════════════════════════════════════════
                📌 ВЕТКА: ${BRANCH}
                ℹ️  CD процесс пропущен (активен только для main)
                📌 Для деплоя сделайте merge в main
                ════════════════════════════════════════════════
                """
            }
        }
    }

    // ========== ДЕЙСТВИЯ ПОСЛЕ ЗАВЕРШЕНИЯ ==========
    post {
        success {
            echo """
            ════════════════════════════════════════════════
            ✅ ПАЙПЛАЙН ВЫПОЛНЕН УСПЕШНО!
            📌 Ветка: ${BRANCH}
            🚀 CD: ${BRANCH == 'main' ? '✅ Выполнен' : '⏭️ Пропущен (не main)'}
            ════════════════════════════════════════════════
            """
        }
        failure {
            echo """
            ════════════════════════════════════════════════
            ❌ ПАЙПЛАЙН ЗАВЕРШИЛСЯ С ОШИБКОЙ!
            📌 Ветка: ${BRANCH}
            🔍 Проверьте логи выше для исправления
            ════════════════════════════════════════════════
            """
        }
    }
}