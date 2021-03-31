from sqlalchemy.orm import Session
import bcrypt

from typing import Union

from db import models, schemas
from middleware.auth import AuthenticationMiddleware


def get_messages(user_id: int):
	#I'm not familiar with pydantic, I'll need to see how to query to see if an id is in a list of id's
	#Too tired to finish this rn...
	db_chats = db.query(models.Chat).filter_by(id=user_id)
	return db_chats