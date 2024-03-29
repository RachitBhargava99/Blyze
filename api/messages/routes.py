from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from db import models, schemas
from db.db import get_db
from .controllers import get_messages, post_message
from users.controllers import get_user_by_username
from etc.decorators import login_required

import json


router = APIRouter()


@router.get('')
@login_required
def get_messages(request: Request):
	user_id = request.state.user_id
	return json.dumps(get_messages(user_id))

@router.post('')
@login_required
def post_message(request: Request, message: schemas.Message):
	user_id = request.state.user_id
	post_message(user_id, message.text, chat_id, 0)