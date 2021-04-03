from sqlalchemy.orm import Session
import bcrypt

from typing import Union

from db import models, schemas
from middleware.auth import AuthenticationMiddleware


def get_messages(user_id: int):
	#chat_ids = db.query(models.)
	#db_chats = db.query(models.Chat).filter_by()
	return db_chats

def get_individual_messages(user_id: int):
	chat_ids = db.query(models.Chat_Individual_Pairs).filter_by(user_id=user_id)
	response = []
	for chat_id in chat_ids:
		messages = db.query(models.Message).filter_by(chat_id=chat_id)
		response.append(messages)
	return response
