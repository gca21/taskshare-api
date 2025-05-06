from pydantic import BaseModel, AfterValidator, Field
from datetime import datetime
from typing import Optional, Annotated
from uuid import uuid4


def str_must_not_be_empty(v: str) -> str:
    if v is not None and str(v).strip() == "":
        raise ValueError(f"Value cannot be empty")
    return v

class UserBase(BaseModel):
    id: Annotated[str, Field(description="Unique identifier of the user")]
    name: Annotated[str, Field(description="Unique name of the user")]

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    id: Annotated[
        str | None,
        Field(default_factory=lambda: str(uuid4()), description="Unique identifier of the user"),
        AfterValidator(str_must_not_be_empty)
    ]
    
    name: Annotated[
        str, 
        Field(description="Unique name of the user"),
        AfterValidator(str_must_not_be_empty)
    ]


class TaskBase(BaseModel):
    id: Annotated[str, Field(description="Unique identifier of the task")]
    title: Annotated[str, Field(description="Unique title of the task")]
    description: Annotated[str, Field(description="Description of the task")]
    due_date: Annotated[datetime, Field(description="Due date of the task")]
    
    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: Annotated[str, Field(description="Unique title of the task")]
    description: Annotated[str | None, Field(default="No description provided", description="Description of the task")]
    due_date: Annotated[datetime | None, Field(description="Due date of the task")]
    assignees: Annotated[list[str] | None, Field(description="Ids of the users assigned to the task")]