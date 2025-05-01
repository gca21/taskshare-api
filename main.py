from fastapi import FastAPI
import models
from database import engine
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}