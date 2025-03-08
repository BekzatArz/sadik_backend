from app import create_app
from flask_migrate import upgrade, Migrate, migrate, init
from sqlalchemy import inspect
from app.extensions import db
import os

app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Берём порт из окружения (если есть)
    app.run(host="0.0.0.0", port=port)
