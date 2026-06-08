from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models.task import TaskStatus



class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    project_id: int
    assigned_to: int
    due_date: Optional[datetime] = None



class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None



class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    project_id: int
    assigned_to: int
    due_date: Optional[datetime]

    class Config:
        from_attributes = True