from db import models
from routers.schemas import FriendRequestCreate, FriendRequestResponse, FriendRequestUpdate
from db.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from auth.oauth2 import get_current_user
from fastapi.exceptions import HTTPException


router = APIRouter(
    prefix="/friend-requests",
    tags=["Friend Requests"],
    responses={404: {"description": "Not found"}},
)



@router.post("/", response_model=FriendRequestResponse, status_code=status.HTTP_201_CREATED)
def send_friend_request(
    request: FriendRequestCreate, 
    db: Session = Depends(get_db), 
    current_user: models.DbUser = Depends(get_current_user)
):
    # Prevent sending friend request to oneself
    if request.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot send a friend request to yourself")
    
    # Check if the receiver exists
    receiver = db.query(models.DbUser).filter(models.DbUser.id == request.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    # Check if the friend request already exists
    existing_request = db.query(models.DbFriendRequest).filter_by(
        sender_id=current_user.id, receiver_id=request.receiver_id).first()
    if existing_request:
        raise HTTPException(status_code=400, detail="Friend request already sent")

    db_request = models.DbFriendRequest(sender_id=current_user.id, receiver_id=request.receiver_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.get("/", response_model=List[FriendRequestResponse])
def get_friend_requests(db: Session = Depends(get_db), current_user: models.DbUser = Depends(get_current_user)):
    requests = db.query(models.DbFriendRequest).filter((models.DbFriendRequest.receiver_id == current_user.id) | (models.DbFriendRequest.sender_id == current_user.id)).all()
    return requests

@router.put("/{request_id}", response_model=FriendRequestResponse)
def update_friend_request(request_id: int, request: FriendRequestUpdate, db: Session = Depends(get_db), current_user: models.DbUser = Depends(get_current_user)):
    db_request = db.query(models.DbFriendRequest).filter(models.DbFriendRequest.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Friend request not found")
    if db_request.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this friend request")

    db_request.status = request.status
    db.commit()
    db.refresh(db_request)
    return db_request