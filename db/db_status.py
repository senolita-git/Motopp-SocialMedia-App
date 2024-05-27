from routers.schemas import StatusPostCreate
from sqlalchemy.orm.session import Session
from db.models import DbStatus
import datetime
from fastapi import HTTPException, status

def create_status(db: Session, request: StatusPostCreate):
    new_status = DbStatus (
        text = request.text,
        timestamp = datetime.datetime.now(),
        user_id = request.creator_id
    )

    db.add(new_status)
    db.commit()
    db.refresh(new_status)
    return new_status

def get_all(db: Session):
    return db.query(DbStatus).all()

#we will create a method to delete a post
def delete(db: Session, id:int, user_id: int):
    status_post = db.query(DbStatus).filter(DbStatus.id == id).first()
    if not status_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'Status with id {id} not found')
    if status_post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only post creator can delete post')
    
    db.delete(status_post)
    db.commit()
    return 'ok'