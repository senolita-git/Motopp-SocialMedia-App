from sqlalchemy.orm import Session
from db.models import DbComment, DbPost, DbStatus, DbUser
from routers.schemas import CommentBase
from datetime import datetime
from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi import status

def create(db: Session, request: CommentBase, current_user: DbUser):
    if request.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username does not match the current user")
    
    if not request.post_id and not request.status_post_id:
        raise ValueError("Either post_id or status_post_id must be provided")
    
    if request.post_id:
        post = db.query(DbPost).filter(DbPost.id == request.post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

    if request.status_post_id:
        status_post = db.query(DbStatus).filter(DbStatus.id == request.status_post_id).first()
        if not status_post:
            raise HTTPException(status_code=404, detail="Status post not found")
        
    user = db.query(DbUser).filter(DbUser.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not match the current user")

    
    new_comment = DbComment(
        text=request.text,
        username=request.username,
        user_id=request.user_id,
        post_id=request.post_id,
        timestamp=datetime.now(),
        status_post_id=request.status_post_id,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all(db: Session, post_id: int, status_post_id: int):
    query = db.query(DbComment)
    
    if(post_id != None):
        query = query.filter(DbComment.id == post_id)
    
    if(status_post_id != None):
        query = query.filter(DbComment.status_post_id == status_post_id)
    
    return query.all()

def get_comment_by_id(db: Session, comment_id: int):
    return db.query(DbComment).filter(DbComment.id == comment_id).first()

def delete(db: Session, comment_id: int):
    comment = db.query(DbComment).filter(DbComment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}