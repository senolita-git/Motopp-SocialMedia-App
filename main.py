from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user, post, comment,status, groups
from fastapi.staticfiles import StaticFiles
from auth import authentication

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(authentication.router) #added to our documentation
app.include_router(status.router)
app.include_router(groups.router)


@app.get("/")
def root():
    return "Hello world!"

models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory = 'images'), name= 'images')