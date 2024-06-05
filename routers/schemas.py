from pydantic import BaseModel
from datetime import datetime
from typing import List, Union, Optional
from db.models import FriendRequestStatus

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    username: str
    email: str
    name: Optional[str] = None
    surname: Optional[str] = None
    bio: Optional[str] = None
    social_media_link: Optional[str] = None
    class Config():
        orm_mode = True

class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creator_id : int

#for postdisplay
class User(BaseModel):
    username: str
    class Config():
        orm_mode = True

#for post display
class Comment(BaseModel):
    text: str
    username: str
    timestamp: datetime
    class Config(): 
        orm_mode = True


class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: User
    class Config(): #we will not get any error when we try to receive postdisplay data type
        orm_mode = True 

#create a new data type for user authentication
class UserAuth(BaseModel):
    id: int
    username: str
    email: str

    #for post display
class Comment(BaseModel):
    text: str
    username: str
    timestamp: datetime
    class Config(): 
        orm_mode = True

class CommentBase(BaseModel):
    username: str
    text: str
    post_id: Optional[int] = None
    status_post_id: Optional[int] = None

class StatusPostCreate(BaseModel):
    text: str
    creator_id: int

class StatusPostDisplay(BaseModel):
    id: int
    text: str
    timestamp: datetime
    user: User
    class Config(): 
        orm_mode = True

class GroupCreate(BaseModel):
    name: str
    description: str

class GroupDisplay(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int

    class Config(): 
        orm_mode = True

class CombinedPost(BaseModel):
    posts: List[Union[PostDisplay, StatusPostDisplay]]
    
    class Config(): 
        orm_mode = True
 
#friend request    
class FriendRequestBase(BaseModel):
    sender_id: int
    receiver_id: int
    status: FriendRequestStatus

    class Config:
        orm_mode = True

class FriendRequestCreate(BaseModel):
    receiver_id: int

class FriendRequestResponse(BaseModel):
    id: int
    sender: User
    receiver: User
    status: FriendRequestStatus

    class Config:
        orm_mode = True

class FriendRequestUpdate(BaseModel):
    status: FriendRequestStatus
    
class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    bio: Optional[str] = None
    social_media_link: Optional[str] = None


#chat schema.

class MessageBase(BaseModel):
    receiver_id: int
    content: str

class MessageDisplay(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True
