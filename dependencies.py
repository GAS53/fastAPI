
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


from services import crud
from property import SECRET_KEY, ALGORITHM
from models import schemas, models

import property

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(crud.fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.is_deleted:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# alchemy func
if property.IS_SQLLITE:
    engin = create_engine(property.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engin = create_engine(property.SQLALCHEMY_DATABASE_URL)

Base = declarative_base()



db_session = sessionmaker(autocommit=False, autoflush=False, bind=engin)


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


