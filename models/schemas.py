from pydantic import BaseModel, PastDate


class Token(BaseModel):
    access_token: str
    token_type: str
    
    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: str | None = None
    
    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    lastname: str | None = None
    email: str | None = None
    phone: int | None = None
    birthday: PastDate | None = None
    is_deleted: bool | None = None
    
    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str