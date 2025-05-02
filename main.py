from fastapi import FastAPI
import models
from database import engine
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
import schemas
import uuid


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # ID unique constraint check
    if user.id is not None:
        existing_user = db.query(models.User).filter(models.User.id == user.id).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="User ID already exists")

        db_user_id = user.id
    else:
        db_user_id = str(uuid.uuid4())
    
    # Name unique constraint check
    existing_user = db.query(models.User).filter(models.User.name == user.name).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User name already exists")
    
    # Create the user in the database
    db_user = models.User(id=db_user_id, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.get("/users/by-name", response_model=schemas.User)
def read_user_by_name(user_name: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == user_name).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: str, user_name: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Name unique constraint check
    existing_user = db.query(models.User).filter(models.User.name == user_name).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User name already exists")
    
    db_user.name = user_name
    db.commit()
    db.refresh(db_user)
    return db_user