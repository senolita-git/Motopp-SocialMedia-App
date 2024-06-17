from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
SQLALCHEMY_DATABASE_URL = 'sqlite:///./socialmedia_app.db'

 
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
 
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
 
Base = declarative_base()

# Drop and recreate tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()