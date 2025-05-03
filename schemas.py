from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


def str_must_not_be_empty(cls, v: str, info) -> str:
    if v is not None and str(v).strip() == "":
        raise ValueError(f"{info.field_name} cannot be empty")
    return v

class User(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    id: Optional[str] = None
    name: str
    
    @field_validator('id')
    def id_must_not_be_empty(cls, v: str, info) -> str:
        return str_must_not_be_empty(cls, v, info)
    
    @field_validator('name')
    def name_must_not_be_empty(cls, v: str, info) -> str:
        return str_must_not_be_empty(cls, v, info)
