from sqlalchemy.orm import Session
from db.models import DbComment
from routers.schemas import CommentBase
from datetime import datetime


def create(db: Session, request: CommentBase):
    new_comment = DbComment(
        text = request.text,
        username = request.username,
        post_id = request.post_id,
        timestamp = datetime. now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all(db: Session, post_id: int):
    query = db.query(DbComment)
    
    if(post_id != None):
        query = query.filter(DbComment.id == post_id)
    
    return query.all()