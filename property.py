SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30
IS_SQLLITE = True
MAX_LEN_BODY_MESSAGE = 256
MAX_LEN_BODY_TITLE = 20

if IS_SQLLITE:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
else:
    SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"