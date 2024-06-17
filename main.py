from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user, post, comment,status, groups, posts, request,chat
from fastapi.staticfiles import StaticFiles
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user.router)
app.include_router(posts.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(authentication.router) #added to our documentation
app.include_router(status.router)
app.include_router(groups.router)
app.include_router(chat.router)
app.include_router(request.router)


@app.get("/")
def root():
    return "Hello world!"

origins = [
  'http://localhost:3000',
  'http://localhost:3001',
  'http://localhost:3002'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)

models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory = 'images'), name= 'images')