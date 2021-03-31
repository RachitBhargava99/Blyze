from sqlalchemy.orm import Session
import bcrypt

from typing import Union

from db import models, schemas
from middleware.auth import AuthenticationMiddleware


def get_user_by_username(db: Session, username: str) -> schemas.User:
    return db.query(models.User).filter_by(username=username).first()


def register_user(db: Session, username: str, pwd: str) -> schemas.User:
    db_user = models.User(username=username, password=pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(db: Session, username: str, pwd: str) -> Union[schemas.User, None]:
    test_hash = str(bcrypt.hashpw(bytes(pwd, encoding='utf8'), b'$2b$12$.Ez2TpYFdXhuIRWIavuklO'))
    db_users = db.query(models.User).filter_by(username=username)
    for curr_user in db_users:
        try:
            if curr_user.password == test_hash:
                curr_user.auth_token = AuthenticationMiddleware.generate_bearer_token({'id': curr_user.id})
                return curr_user
        except ValueError:
            continue
    return None


def get_user_by_id(db: Session, user_id: int) -> schemas.User:
    return db.query(models.User).filter_by(id=user_id).first()
