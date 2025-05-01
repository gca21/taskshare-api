from fastapi import FastAPI
import models
from database import engine
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
import schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user