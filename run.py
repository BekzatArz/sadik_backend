from app import create_app
from flask_migrate import upgrade
import os

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        upgrade()  # Выполняем миграции

    port = int(os.environ.get("PORT", 80))  # Берём порт из окружения (если есть)
    app.run(host="0.0.0.0", port=port)
