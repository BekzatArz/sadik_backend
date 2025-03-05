from app import create_app
from flask_migrate import upgrade, migrate, init
import os

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        try:
            # Инициализация папки с миграциями (если её нет)
            if not os.path.exists("migrations"):
                init()

            # Создание новых миграций
            migrate()

            # Применение миграций к БД
            upgrade()
        except Exception as e:
            print(f"Ошибка при миграции: {e}")

    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)
