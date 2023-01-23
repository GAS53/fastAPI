from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import property
from models import schemas
from services import crud, auth
import dependencies
import services


router = APIRouter()


@router.post('/registry')
def make_new_user(user: schemas.UserInDB, db: Session = Depends(dependencies.get_db)):
    print(f'0type {type(db)} {db}')
    user1 = crud.get_user_by_name(db, user.username)
    user2 = crud.get_user_by_email(db, user.email)
    user3 = crud.get_user_by_phone(db, user.phone)
    if user1 or user2 or user3:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='user ulready registred')
    crud.save_user(db, user)
    
@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=property.TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]