from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from db.models import DbMessage, DbUser
from routers.schemas import MessageBase, MessageDisplay
from auth.oauth2 import get_current_user
from db import db_message

router = APIRouter(
    prefix='/chat',
    tags=['chat']
)

@router.post('/', response_model=MessageDisplay)
def send_message(
    request: MessageBase,
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(get_current_user)
):
    return db_message.create(db, request, current_user.id)

@router.get('/', response_model=List[MessageDisplay])
def get_messages(
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(get_current_user)
):
    return db_message.get_messages(db, current_user.id)
