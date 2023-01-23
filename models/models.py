import datetime


from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String, Date
import property


from dependencies import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String(36), nullable=False, unique=True)
    lastname = Column(String(36))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone = Column(Integer, unique=True, nullable=False)
    birthday = Column(Date)
    created = Column(Date, default=datetime.datetime.now())
    is_deleted = Column(Boolean, default=False)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    from_user = Column(Integer, ForeignKey('users.id'))
    created = Column(Date, default=datetime.datetime.now())
    body = Column(String(property.MAX_LEN_BODY_MESSAGE))
    title = Column(String(property.MAX_LEN_BODY_TITLE))


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    to_message_id = Column(Integer, ForeignKey('messages.id'))
    from_user = Column(Integer, ForeignKey('users.id'))
    created = Column(Date)
    is_positive = Column(Boolean, default=True)
    

'''"johndoe": {
        "username": "johndoe",
        "lastname": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }'''