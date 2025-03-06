import os
from app import create_app
from flask_migrate import upgrade, migrate, init

app = create_app()

def run_migrations():
    with app.app_context():
        # Проверяем, есть ли директория "migrations", если нет — инициализируем Alembic
        if not os.path.exists("migrations"):
            init()

        # Создаём новую миграцию
        migrate(message="Auto migration")

        # Применяем миграцию
        upgrade()