from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    priority: Optional[int] = 1
    note: Optional[str] = None
    is_completed: bool = False

class TaskCreate(TaskBase):
    pass
class TaskResponse(TaskBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    tasks: List[TaskResponse] = []
    class Config:
        from_attributes = True