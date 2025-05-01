from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base


task_assignments = Table(
    "task_assignments",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    tasks = relationship("Task", secondary=task_assignments, back_populates="assignees")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    due_date = Column(DateTime, nullable=True)
    assignees = relationship("User", secondary=task_assignments, back_populates="tasks")
