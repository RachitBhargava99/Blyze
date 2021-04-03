from sqlalchemy.orm import Session
import bcrypt

from typing import Union

from db import models, schemas
from middleware.auth import AuthenticationMiddleware


def get_messages(user_id: int):
	db_chats = []
	org_chats = get_organization_messages(user_id)
	proj_chats = get_project_messages(user_id)
	ind_chats = get_individual_messages(user_id)
	for message in org_chats:
		db_chats.append(message)
	for message in proj_chats:
		db_chats.append(message)
	for message in ind_chats:
		db_chats.append(message)
	return db_chats

def get_individual_messages(user_id: int):
	chat_ids = db.query(models.Chat_Individual_Pairs).filter_by(user_id=user_id)
	response = []
	for chat_id in chat_ids:
		messages = db.query(models.Message).filter_by(chat_id=chat_id)
		response.append(messages)
	return response

def get_project_messages(user_id: int):
	chat_ids = db.query(models.Project_Membership).filter_by(user_id=user_id)
	response = []
	for chat_id in chat_ids:
		messages = db.query(models.Message).filter_by(chat_id=chat_id)
		response.append(messages)
	return response

def get_organization_messages(user_id: int):
	chat_ids = db.query(models.Org_Membership).filter_by(user_id=user_id)
	response = []
	for chat_id in chat_ids:
		messages = db.query(models.Message).filter_by(chat_id=chat_id)
		response.append(messages)
	return response
