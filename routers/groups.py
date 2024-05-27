from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import get_db
from routers.schemas import UserAuth, GroupCreate, GroupDisplay, UserDisplay
from auth.oauth2 import get_current_user
from db.models import DbGroup


router = APIRouter( prefix="/groups", tags=["groups"])


@router.post("/groups/", response_model=GroupDisplay)
def create_group(group: GroupCreate, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    db_group = DbGroup(name=group.name, description=group.description, owner_id=current_user.id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.post("/groups/{group_id}/join", response_model=GroupDisplay)
def join_group(group_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    group = db.query(DbGroup).filter(DbGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    group.members.append(current_user)
    db.commit()
    return group

@router.get("/groups/{group_id}/members", response_model=List[UserDisplay])
def list_group_members(group_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    group = db.query(DbGroup).filter(DbGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group.members