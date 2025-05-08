from fastapi import APIRouter, Depends, HTTPException
from app import models, schemas
from app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Tasks"])


@router.get("/tasks/", response_model=list[schemas.TaskBase])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_tasks = db.query(models.Task).offset(skip).limit(limit).all()
    return db_tasks

@router.post("/tasks/", response_model=schemas.TaskBase)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    # Title unique constraint check
    existing_task = db.query(models.Task).filter(models.Task.title == task.title).first()
    if existing_task:
        raise HTTPException(status_code=409, detail="Task title already exists")
    
    # Create the task in the database
    db_task = models.Task(title = task.title, description = task.description, due_date = task.due_date)
    
    if task.assignees:
        db_assignees = db.query(models.User).filter(models.User.id.in_(task.assignees)).all()
        if len(db_assignees) != len(task.assignees):
                raise HTTPException(status_code=400, detail="Some users IDs are invalid.")
    else:
        db_assignees = []
        
    db_task.assignees = db_assignees
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/tasks/{task_id}", response_model=schemas.TaskBase)
def update_task(task_id: str, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Title unique constraint check
    existing_task = db.query(models.Task).filter(models.Task.title == task.title).first()
    if existing_task:
        raise HTTPException(status_code=409, detail="Task title already exists")
    
    db_task.title = task.title
    db_task.description = task.description
    db_task.due_date = task.due_date
    db_task.assignees = task.assignees
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}", response_model=schemas.TaskBase)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return db_task