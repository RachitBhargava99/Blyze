from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import register_user, login_user, get_user_by_username
from etc.decorators import login_required


router = APIRouter()


@router.put('', response_model=schemas.User)
def register_user_route(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username) is not None:
        raise HTTPException(status_code=409, detail="User Already Exists")
    db_user = register_user(db, user.username, user.password)
    return db_user


@router.post('', response_model=schemas.UserAuthenticated)
def login_user_route(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = login_user(db, user.username, user.password)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Login Attempt Failed")
    return db_user


@router.get('')
@login_required
def get_user_id(request: Request):
    user_id = request.state.user_id
    # print(user_id)
    return user_id
