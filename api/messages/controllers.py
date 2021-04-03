from sqlalchemy.orm import Session
import bcrypt

from typing import Union

from db import models, schemas
from middleware.auth import AuthenticationMiddleware


def get_messages(user_id: int):
	chat_ids = db.query(models.)
	#db_chats = db.query(models.Chat).filter_by()
	return db_chats