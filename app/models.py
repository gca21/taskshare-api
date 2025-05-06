from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base


task_assignments = Table(
    "task_assignments",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("user_id", String, ForeignKey("users.id"))
)

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    tasks = relationship("Task", secondary=task_assignments, back_populates="assignees")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    assignees = relationship("User", secondary=task_assignments, back_populates="tasks")
