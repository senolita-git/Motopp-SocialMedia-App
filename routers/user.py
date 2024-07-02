from fastapi import APIRouter, Depends
from routers.schemas import UserDisplay, UserBase, UserUpdate, UserAuth,PostDisplay,StatusPostDisplay,CommentBase,User, FriendUserDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
from db.models import DbUser,DbComment,DbPost,DbStatus, DbFriendRequest, FriendRequestStatus
from auth.oauth2 import get_current_user
from fastapi.exceptions import HTTPException
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

router = APIRouter(
    prefix = '/user',
    tags=['user']
)

@router.post('',response_model=UserDisplay)
def create_user(request: UserBase, db: Session=Depends(get_db)):
    return db_user.create_user(db, request)

@router.get("/{user_id}", response_model=UserDisplay)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

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

@router.delete('/{user_id}', response_model=UserDisplay)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this user")
    
    db.delete(user)
    db.commit()
    return user

@router.get("/{user_id}/posts")
def get_user_posts(user_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    image_posts = db.query(DbPost).filter(DbPost.user_id == user_id).all()
    image_post_list = [PostDisplay(
        id=post.id,
        image_url=post.image_url,
        image_url_type=post.image_url_type,
        caption=post.caption,
        timestamp=post.timestamp,
        user_id=post.user_id,
        user=User(id=post.user.id, username=post.user.username)
    ) for post in image_posts]

    status_posts = db.query(DbStatus).filter(DbStatus.user_id == user_id).all()
    status_post_list = [StatusPostDisplay(
        id=post.id,
        text=post.text,
        timestamp=post.timestamp,
        user_id=post.user_id,
        user=User(id=post.user.id, username=post.user.username)
    ) for post in status_posts]

    combined_posts = image_post_list + status_post_list
    combined_posts.sort(key=lambda x: x.timestamp, reverse=True)

    return combined_posts

@router.get("/{user_id}/comments", response_model=List[CommentBase])
def get_user_comments(user_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    comments = db.query(DbComment).filter(DbComment.user_id == user_id).all()
    return comments

@router.get("/{user_id}/friends", response_model=List[FriendUserDisplay])
def get_user_friends(user_id: int, db: Session = Depends(get_db)):
    # Fetch all friends where the status is 'accepted'
    sent_friends = db.query(DbUser).join(DbFriendRequest, DbFriendRequest.receiver_id == DbUser.id).filter(DbFriendRequest.sender_id == user_id, DbFriendRequest.status == FriendRequestStatus.ACCEPTED).all()
    received_friends = db.query(DbUser).join(DbFriendRequest, DbFriendRequest.sender_id == DbUser.id).filter(DbFriendRequest.receiver_id == user_id, DbFriendRequest.status == FriendRequestStatus.ACCEPTED).all()

    friends = sent_friends + received_friends
    return friends

@router.post("/profile-picture")
def upload_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(get_current_user)
):
    if not file.filename.endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

    file_path = f"static/profile_pictures/{current_user.id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    current_user.profile_picture_url = file_path
    db.commit()
    db.refresh(current_user)
    return {"profile_picture_url": file_path}