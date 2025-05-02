from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional


def user_name_must_not_be_empty(v: str) -> str:
    if str(v).strip() == "":
        raise ValueError("Name cannot be empty")
    return v

def user_id_must_not_be_empty(v: str) -> str:
    if v is not None and str(v).strip() == "":
        raise ValueError("Id cannot be empty")
    return v

class User(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    id: Optional[str] = None
    name: str
    
    _validate_id = validator("id")(user_id_must_not_be_empty)
    _validate_name = validator("name")(user_name_must_not_be_empty)