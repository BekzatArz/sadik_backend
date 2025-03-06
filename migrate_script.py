import os
from app import create_app
from flask_migrate import upgrade, migrate, init
from flask_migrate import Migrate
import subprocess

app = create_app()

def run_migrations():
    with app.app_context():
        # Проверяем, есть ли директория "migrations", если нет — инициализируем Alembic
        if not os.path.exists("migrations"):
            init()

        # Создаём новую миграцию
        # Важно не передавать сообщение напрямую через migrate, используем команду для миграции
        subprocess.run(["flask", "db", "migrate", "-m", "Auto migration"], check=True)

        # Применяем миграцию
        subprocess.run(["flask", "db", "upgrade"], check=True)

if __name__ == "__main__":
    run_migrations()
