from app import create_app
from flask_migrate import upgrade
from migrate_script import run_migrations
from app.extensions import db
import os

app = create_app()
@app.route('/tables')
def list_tables():
    # Получаем список таблиц
    with app.app_context():
        tables = db.engine.table_names()  # Получаем все таблицы из базы данных
        return {"tables": tables}

if __name__ == "__main__":
    with app.app_context():
        run_migrations()  # Выполняем миграции

    port = int(os.environ.get("PORT", 80))  # Берём порт из окружения (если есть)
    app.run(host="0.0.0.0", port=port)
