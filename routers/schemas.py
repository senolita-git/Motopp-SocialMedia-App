from pydantic import BaseModel
from datetime import datetime
from typing import List, Union, Optional
from db.models import FriendRequestStatus

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    id : int
    username: str
    email: str
    name: Optional[str] = None
    surname: Optional[str] = None
    bio: Optional[str] = None
    social_media_link: Optional[str] = None
    profile_picture_url: Optional[str] = None
    class Config():
        from_attributes = True

class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creator_id : int

#for postdisplay
class User(BaseModel):
    username: str
    class Config():
        from_attributes = True

#for post display
class Comment(BaseModel):
    text: str
    username: str
    timestamp: datetime
    class Config(): 
        from_attributes = True


class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: User
    user_id: int
    class Config(): #we will not get any error when we try to receive postdisplay data type
        from_attributes = True 

#create a new data type for user authentication
class UserAuth(BaseModel):
    id: int
    username: str
    email: str

    #for post display
class Comment(BaseModel):
    id: int
    text: str
    username: str
    timestamp: datetime
    class Config(): 
        from_attributes = True

class CommentBase(BaseModel):
    user_id: int
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
    user_id: int
    class Config(): 
        from_attributes = True

class GroupCreate(BaseModel):
    name: str
    description: str

class GroupDisplay(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int

    class Config(): 
        from_attributes = True

class CombinedPost(BaseModel):
    posts: List[Union[PostDisplay, StatusPostDisplay]]
    
    class Config(): 
        from_attributes = True
 
#friend request    
class FriendRequestBase(BaseModel):
    sender_id: int
    receiver_id: int
    status: FriendRequestStatus

    class Config:
        from_attributes = True

class FriendRequestCreate(BaseModel):
    receiver_id: int

class FriendRequestResponse(BaseModel):
    id: int
    sender: User
    receiver: User
    status: FriendRequestStatus

    class Config:
        from_attributes = True

class FriendRequestUpdate(BaseModel):
    status: FriendRequestStatus

class FriendUserDisplay(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    surname: Optional[str] = None

    class Config():
        from_attributes = True
    
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
        from_attributes = True

