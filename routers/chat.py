from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from db.models import DbMessage, DbUser
from routers.schemas import MessageBase, MessageDisplay
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/chat',
    tags=['chat']
)

@router.post('/', response_model=MessageDisplay)
def send_message(request: MessageBase, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    new_message = DbMessage(
        sender_id=current_user.id,
        receiver_id=request.receiver_id,
        content=request.content,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

@router.get('/{receiver_id}', response_model=List[MessageDisplay])
def get_messages(receiver_id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    messages = db.query(DbMessage).filter(
        (DbMessage.sender_id == current_user.id) & (DbMessage.receiver_id == receiver_id) |
        (DbMessage.sender_id == receiver_id) & (DbMessage.receiver_id == current_user.id)
    ).all()
    return messages
