import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from db.models import Base, DbUser, DbPost, DbComment, DbStatus, DbGroup, DbFriendRequest, FriendRequestStatus
from db.database import SQLALCHEMY_DATABASE_URL

# Create a new database session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
session = Session(bind=engine)

# Add sample users
user1 = DbUser(username='user1', email='user1@example.com', password='hashedpassword1')
user2 = DbUser(username='user2', email='user2@example.com', password='hashedpassword2')
user3 = DbUser(username='user3', email='user3@example.com', password='hashedpassword3')
session.add(user1)
session.add(user2)
session.add(user3)
session.commit()

# Add sample posts
post1 = DbPost(image_url='http://example.com/image1.jpg', image_url_type='url', caption='First post', timestamp=datetime.now(), user_id=user1.id)
post2 = DbPost(image_url='http://example.com/image2.jpg', image_url_type='url', caption='Second post', timestamp=datetime.now(), user_id=user2.id)
session.add(post1)
session.add(post2)
session.commit()

# Add sample status posts
status1 = DbStatus(text='Feeling great!', timestamp=datetime.now(), user_id=user1.id)
status2 = DbStatus(text='Had a wonderful day!', timestamp=datetime.now(), user_id=user2.id)
session.add(status1)
session.add(status2)
session.commit()

# Add sample comments
comment1 = DbComment(text='Nice post!', username=user2.username, timestamp=datetime.now(), post_id=post1.id)
comment2 = DbComment(text='Awesome status!', username=user1.username, timestamp=datetime.now(), status_post_id=status1.id)
session.add(comment1)
session.add(comment2)
session.commit()

# Add sample groups
group1 = DbGroup(name='Group 1', description='This is the first group', owner_id=user1.id)
group2 = DbGroup(name='Group 2', description='This is the second group', owner_id=user2.id)
session.add(group1)
session.add(group2)
session.commit()

# Add members to groups
group1.members.append(user2)
group1.members.append(user3)
group2.members.append(user1)
group2.members.append(user3)
session.commit()

# Add sample friend requests
friend_request1 = DbFriendRequest(sender_id=user1.id, receiver_id=user2.id, status=FriendRequestStatus.PENDING)
friend_request2 = DbFriendRequest(sender_id=user2.id, receiver_id=user3.id, status=FriendRequestStatus.ACCEPTED)
session.add(friend_request1)
session.add(friend_request2)
session.commit()

# Close the session
session.close()

print("Database populated with test data.")
