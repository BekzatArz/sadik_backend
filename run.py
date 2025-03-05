from app import create_app
from app.extensions import db
import os

app = create_app()

# Функция для создания таблиц в базе данных
def create_tables():
    with app.app_context():
        db.create_all()  # Создаем все таблицы в базе данных

if __name__ == "__main__":
    create_tables()  # Выполняем создание таблиц

    port = int(os.environ.get("PORT", 80))  # Берём порт из окружения (если есть)
    app.run(host="0.0.0.0", port=port)
