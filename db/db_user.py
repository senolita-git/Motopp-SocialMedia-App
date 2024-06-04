#to create user
from routers.schemas import UserBase, UserUpdate
from sqlalchemy.orm.session import Session
from db.models import DbUser
from db.hashing import Hash
from fastapi import HTTPException, status

def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password) #we need to hash the password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first() # we are gonna get the first element
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'User with username {username} not found')
    return user

def update(db: Session, user_id: int, request: UserUpdate):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")

    if request.name is not None:
        user.name = request.name
    if request.surname is not None:
        user.surname = request.surname
    if request.bio is not None:
        user.bio = request.bio
    if request.social_media_link is not None:
        user.social_media_link = request.social_media_link

    db.commit()
    db.refresh(user)
    return user