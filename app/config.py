class Config:
    # Используем строку подключения, которую вам дал Railway
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:LgRnVpYsugrREeFFFuGBRCrRhIjiGyOP@postgres-1twg.railway.internal:5432/railway"
    
    # Отключаем отслеживание изменений объектов SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Секретный ключ для обеспечения безопасности в приложении
    SECRET_KEY = 'BexBexBex'