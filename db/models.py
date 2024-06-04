from db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Table, Enum as SQLEnum
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

group_membership = Table('group_membership', Base.metadata,
                         Column('user_id', Integer, ForeignKey('user.id'), primary_key = True),
                         Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
                         )

class DbUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    name = Column(String)  # Add name field
    surname = Column(String)  # Add surname field
    bio = Column(String) # Add bio field
    social_media_link = Column(String)

    items = relationship('DbPost', back_populates='user')
    status = relationship('DbStatus', back_populates='user')
    owned_groups = relationship('DbGroup', back_populates='owner')
    groups = relationship('DbGroup', secondary=group_membership, back_populates='members')

#we will create another table for creating post
class DbPost(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    image_url_type = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('DbUser', back_populates='items')
    comments = relationship('DbComment', back_populates='post')

class DbComment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey('post.id'))
    status_post_id = Column(Integer, ForeignKey('status_post.id'))
    
    post = relationship("DbPost", back_populates="comments")
    status_post = relationship('DbStatus', back_populates='comments')

class DbStatus(Base):
    __tablename__ = 'status_post'
    id = Column(Integer, primary_key=True, index=True)
    text =Column(String, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime)
    user = relationship('DbUser', back_populates='status')
    comments = relationship('DbComment', back_populates='status_post')

class DbGroup(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('user.id'))

    owner = relationship('DbUser', back_populates='owned_groups')
    members = relationship('DbUser', secondary=group_membership, back_populates='groups')

class FriendRequestStatus(PyEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DENIED = "denied"

class DbFriendRequest(Base):
    __tablename__ = 'friend_request'
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('user.id'))
    receiver_id = Column(Integer, ForeignKey('user.id'))
    status = Column(SQLEnum(FriendRequestStatus), default=FriendRequestStatus.PENDING)

    sender = relationship('DbUser', foreign_keys=[sender_id])
    receiver = relationship('DbUser', foreign_keys=[receiver_id])