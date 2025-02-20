class Config:
    DB_HOST = "amvera-bexslay-cnpg-flaskdb-rw"
    DB_USER = "bexy"
    DB_PASSWORD = "Beka2007"
    DB_NAME = "sadik"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'BexBexBex' 