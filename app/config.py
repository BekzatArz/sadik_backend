class Config:
    DB_HOST = "postgres-1twg.railway.internal:5432"
    DB_USER = "postgres"
    DB_PASSWORD = "LgRnVpYsugrREeFFFuGBRCrRhIjiGyOP"
    DB_NAME = "railway"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'BexBexBex'
