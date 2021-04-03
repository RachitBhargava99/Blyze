from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from db import models, schemas
from db.db import get_db
from .controllers import get_messages
from etc.decorators import login_required


router = APIRouter()


@router.get('')
@login_required
def get_messages(request: Request):
	user_id = request.state.user_id
	return get_messages(user_id)