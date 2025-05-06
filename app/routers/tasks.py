from fastapi import APIRouter, Depends, HTTPException
from app import models, schemas
from app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/tasks/", response_model=list[schemas.TaskBase])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_tasks = db.query(models.Task).offset(skip).limit(limit).all()
    return db_tasks