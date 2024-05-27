from db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Table
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

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
    post = relationship("DbPost", back_populates="comments")

class DbStatus(Base):
    __tablename__ = 'status_post'
    id = Column(Integer, primary_key=True, index=True)
    text =Column(String, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime)
    user = relationship('DbUser', back_populates='status')

class DbGroup(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('user.id'))

    owner = relationship('DbUser', back_populates='owned_groups')
    members = relationship('DbUser', secondary=group_membership, back_populates='groups')
