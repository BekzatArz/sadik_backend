from app import create_app
from flask_migrate import upgrade, Migrate, migrate, init

from app.extensions import db
import subprocess
import os

app = create_app()
migrate = Migrate(app, db)

def run_migrations():
    with app.app_context():
        # Проверяем, существует ли папка миграций, если нет, то инициализируем
        if not os.path.exists("migrations"):
            print("Папка миграций не существует. Инициализация...")
            init()

        # Получаем все таблицы в базе данных
        existing_tables = db.engine.table_names()

        # Проверка, если таблицы уже существуют, выполняем миграцию
        if existing_tables:
            print("Таблицы уже существуют. Проверка на изменения...")

            # Запуск миграции, если изменения есть
            subprocess.run(["flask", "db", "migrate", "-m", "Auto migration"], check=True)

            # Применение миграций, если они были созданы
            subprocess.run(["flask", "db", "upgrade"], check=True)
            print("Миграции успешно применены.")
        else:
            # Если таблиц нет, создаем их через db.create_all()
            print("Таблицы не найдены, создание через db.create_all()...")
            db.create_all()
            print("Таблицы успешно созданы.")

if __name__ == "__main__":
    run_migrations()
    port = int(os.environ.get("PORT", 80))  # Берём порт из окружения (если есть)
    app.run(host="0.0.0.0", port=port)
