from sqlalchemy import create_engine, select, update, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from models import schemas, models
from services import auth
import property


engine = create_engine(property.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
from sqlalchemy.orm import Session


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "lastname": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

def get_user(db: Session, username: str):
    query = select(models.User).where(models.User.username == username)
    db_user = db.execute(query).fetchone()
    if db_user:
        db_user = db_user[0]
        user = schemas.UserInDB(username=db_user.username, lastname=db_user.lastname,
        email=db_user.email, phone=db_user.phone, birthday=db_user.birthday,
        is_deleted=db_user.is_deleted, hashed_password=db_user.hashed_password)
        return user
    
    
def get_user_by_name(db: Session, name: str):
    query = select(models.User).where(models.User.username == name)
    db_user = db.execute(query).first()
    if db_user:
        db_user = db_user[0]
        user = schemas.User(username=db_user.username, lastname=db_user.lastname,
        email=db_user.email, phone=db_user.phone, birthday=db_user.birthday,
        is_deleted=db_user.is_deleted)
        return user


def get_user_by_email(db: Session, email: str):
    query = select(models.User).where(models.User.email == email)
    db_user = db.execute(query).first()
    print(db_user)
    if db_user:
        db_user = db_user[0]
        user = schemas.User(username=db_user.username, lastname=db_user.lastname,
        email=db_user.email, phone=db_user.phone, birthday=db_user.birthday,
        is_deleted=db_user.is_deleted)
        return user


def get_user_by_phone(db: Session, phone: str):
    query = select(models.User).where(models.User.phone == phone)
    db_user = db.execute(query).first()
    if db_user:
        db_user = db_user[0]
        user = schemas.User(username=db_user.username, lastname=db_user.lastname,
        email=db_user.email, phone=db_user.phone, birthday=db_user.birthday,
        is_deleted=db_user.is_deleted)
        return user

def save_user(db: Session, user: schemas.User):
    query = insert(models.User).values(username=user.username,
    lastname=user.lastname, email=user.email, phone=user.phone, 
    birthday=user.birthday, is_deleted=user.is_deleted, 
    hashed_password=auth.get_password_hash(user.hashed_password))
    db_user = db.execute(query)
    db.commit()
    return db_user
