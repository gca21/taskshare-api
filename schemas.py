from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class User(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None  # New field

class TaskCreate(TaskBase):
    assignee_ids: List[int]

class Task(TaskBase):
    id: int
    assignees: List[User] = []

    class Config:
        from_attributes = True
