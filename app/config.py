# class Config:
#     DB_HOST = "127.0.0.1"
#     DB_USER = "postgres"
#     DB_PASSWORD = "postgres"
#     DB_NAME = "postgres"
#     SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = 'BexBexBex' 



class Config:
    DB_HOST = "amvera-bexslay-cnpg-flaskdb-rw"
    DB_USER = "bexy"
    DB_PASSWORD = "Beka2007"
    DB_NAME = "sadik"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'BexBexBex' 
