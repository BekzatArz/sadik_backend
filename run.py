from app import create_app
<<<<<<< HEAD
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
=======
from flask_migrate import upgrade
import os
>>>>>>> 26e3c7296ab998291bca4842a3ff4881e81b2e56

app = create_app()

if __name__ == "__main__":
<<<<<<< HEAD
=======
    with app.app_context():
        upgrade()  # Выполняем миграции

>>>>>>> 26e3c7296ab998291bca4842a3ff4881e81b2e56
    port = int(os.environ.get("PORT", 80))  # Берём порт из окружения (если есть)
    app.run(host="0.0.0.0", port=port)
