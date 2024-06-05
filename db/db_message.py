from db.models import DbFriendRequest, DbMessage
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from routers.schemas import MessageBase
from datetime import datetime


def create(db: Session, request: MessageBase, sender_id: int):
    # Check if the sender and receiver are friends
    friendship = db.query(DbFriendRequest).filter(
        ((DbFriendRequest.sender_id == sender_id) & (DbFriendRequest.receiver_id == request.receiver_id)) |
        ((DbFriendRequest.receiver_id == sender_id) & (DbFriendRequest.sender_id == request.receiver_id))
    ).filter(DbFriendRequest.status == "ACCEPTED").first()

    if not friendship:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only send messages to friends")

    # Create a new message
    new_message = DbMessage(
        sender_id=sender_id,
        receiver_id=request.receiver_id,
        content=request.content,
        timestamp=datetime.now()
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def get_messages(db: Session, user_id: int):
    # Retrieve messages where the user is either the sender or the receiver
    return db.query(DbMessage).filter(
        (DbMessage.sender_id == user_id) | (DbMessage.receiver_id == user_id)
    ).all()