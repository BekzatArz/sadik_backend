from app import create_app
import os
import logging

# Настройка логирования
logging.basicConfig(
    filename='/app/app.log',  # Путь до лог-файла в контейнере
    level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Формат записи в лог
)

# Логирование при старте приложения
logging.info("Application is starting...")

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))  # Берём порт из окружения (если есть)
    app.run(host="0.0.0.0", port=port)
