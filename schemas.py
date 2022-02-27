from datetime import datetime
import datetime
from typing import Optional
from pydantic import BaseModel, validator, constr

class ToDo(BaseModel):
    task: str
    due_date: datetime.date
    is_completed: Optional[str] = "No"
    created_by: Optional[str] = None
    assigned_to: Optional[str] = None
    group_name: Optional[str] = None

class User(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None

    @validator('username')
    def validate_username(u):
        if u=="":
            raise ValueError("Username is invalid. Use a valid username.")
        return u

    @validator('password')
    def validate_password(p):
        if p=="":
            raise ValueError("Password is invalid. Use a valid password.")
        return p