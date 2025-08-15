from pydantic import BaseModel, Field, constr
from typing import Optional, List
from uuid import UUID
from models import TaskStatus, TaskPriority
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id: UUID
    username: str
    email: str
    is_admin: bool

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: constr(min_length=5, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.pending
    priority: Optional[TaskPriority] = TaskPriority.medium
    assignee_id: Optional[UUID]

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[constr(min_length=5, max_length=255)]
    description: Optional[str]
    status: Optional[TaskStatus]
    priority: Optional[TaskPriority]
    assignee_id: Optional[UUID]

class TaskRead(TaskBase):
    id: UUID
    created_at: datetime
    deleted: bool = False

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str
    created_by: UUID

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True