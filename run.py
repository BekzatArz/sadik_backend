from app import create_app
from flask_migrate import upgrade, Migrate, migrate, init
from sqlalchemy import inspect
from app.extensions import db
import os

app = create_app()
migrate = Migrate(app, db)

def run_migrations():
    with app.app_context():
        migrations_path = os.path.join(os.getcwd(), "migrations")

        # Проверяем, существует ли папка миграций, если нет, то инициализируем
        if not os.path.exists(migrations_path):
            print("Папка миграций не найдена. Инициализируем...")
            init(directory=migrations_path)  # Правильный вызов init()

        # Проверяем, есть ли таблицы в базе данных
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()

        if existing_tables:
            print("Таблицы найдены. Проверка на изменения...")
            migrate(message="Auto migration")  # Создаём миграции
            upgrade()  # Применяем миграции
            print("Миграции успешно применены.")
        else:
            print("Таблицы не найдены. Создаём...")
            db.create_all()
            print("Таблицы успешно созданы.")

if __name__ == "__main__":
    run_migrations()
    port = int(os.environ.get("PORT", 5000))  # Берём порт из окружения (если есть)
    app.run(host="0.0.0.0", port=port)
