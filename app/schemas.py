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
