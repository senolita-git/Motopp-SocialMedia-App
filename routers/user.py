from fastapi import APIRouter, Depends
from routers.schemas import UserDisplay, UserBase, UserUpdate
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
from db.models import DbUser
from auth.oauth2 import get_current_user
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix = '/user',
    tags=['user']
)

@router.post('',response_model=UserDisplay)
def create_user(request: UserBase, db: Session=Depends(get_db)):
    return db_user.create_user(db, request)

@router.put('/{user_id}', response_model=UserDisplay)
def update_user(
    user_id: int,
    request: UserUpdate,
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    return db_user.update(db, user_id, request)