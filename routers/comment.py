from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_comment
from routers.schemas import CommentBase, UserAuth
from auth.oauth2 import get_current_user
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix = '/comment',
    tags = ['comment']
)

@router.get('/')
def comments(post_id: Optional[int] = None, status_post_id: Optional[int] = None, 
    db: Session = Depends(get_db)):
    return db_comment.get_all(db, post_id, status_post_id)

@router.post('')
def create(request: CommentBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    try:
        return db_comment.create(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete('/{comment_id}')
def delete(comment_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    comment = db_comment.get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.username != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    return db_comment.delete(db, comment_id)