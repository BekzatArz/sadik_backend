from app import create_app, db
from flask_migrate import upgrade, migrate, init
import os

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        try:
            # Проверяем, есть ли папка миграций
            if not os.path.exists("migrations"):
                init()  # Создаём папку с миграциями

            migrate()  # Генерируем миграции
            upgrade()  # Применяем миграции
            print("✅ Миграции успешно применены!")

            # Проверяем, есть ли таблица users
            result = db.session.execute("SELECT * FROM users LIMIT 1;")
            print("✅ Таблица users найдена!")
        except Exception as e:
            print(f"❌ Ошибка при миграции: {e}")

    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)
