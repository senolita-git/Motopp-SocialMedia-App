from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from routers.schemas import StatusPostCreate,StatusPostDisplay
from db.database import get_db
from db import db_status
from routers.schemas import UserAuth
from auth.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix = '/status',
    tags = ['status']
)

@router.post('', response_model=StatusPostDisplay)
def create(request: StatusPostCreate, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_status.create_status(db, request)
 
@router.delete('/{id}') # id of the post
def delete(id: int, db:Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_status.delete(db, id, current_user.id)