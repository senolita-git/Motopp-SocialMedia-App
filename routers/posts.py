from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.models import DbPost, DbStatus  # Import your models and get_db dependency
from db.database import get_db
from routers.schemas import CombinedPost, PostDisplay, StatusPostDisplay, User  # Import your schema

router = APIRouter(
    prefix = '/posts',
    tags = ['posts']
)

@router.get('/')#, response_model=CombinedPost)
def get_all_posts(db: Session = Depends(get_db)):
    # Fetch all image posts
    image_posts = db.query(DbPost).all()
    image_post_list = [PostDisplay(id=post.id,
        image_url=post.image_url,
        image_url_type=post.image_url_type,
        caption=post.caption,
        timestamp=post.timestamp,
        user=User(username = post.user.username)
        )
                       for post in image_posts]

    # Fetch all status posts
    status_posts = db.query(DbStatus).all()
    status_post_list = [StatusPostDisplay(id=post.id,
        text=post.text,
        timestamp=post.timestamp,
        user=User(username = post.user.username))
                        for post in status_posts]

    # Combine both lists
    combined_posts = image_post_list + status_post_list

    # Sort by timestamp
    combined_posts.sort(key=lambda x: x.timestamp, reverse=True)

    return combined_posts