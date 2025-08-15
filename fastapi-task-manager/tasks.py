from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from models import Task, Comment
from schemas import TaskCreate, TaskUpdate, TaskRead, CommentCreate, CommentRead
from uuid import UUID

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Create task
@router.post("/", response_model=TaskRead)
async def create_task(task: TaskCreate, session: AsyncSession = Depends(get_session)):
    new_task = Task(**task.dict())
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task

# Get all tasks
@router.get("/", response_model=list[TaskRead])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task).where(Task.deleted == False))
    return result.scalars().all()

# Get task by ID
@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task).where(Task.id == task_id, Task.deleted == False))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(404, "Task not found")
    return task

# Update task
@router.put("/{task_id}", response_model=TaskRead)
async def update_task(task_id: UUID, task_update: TaskUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task).where(Task.id == task_id, Task.deleted == False))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(404, "Task not found")
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)
    await session.commit()
    await session.refresh(task)
    return task

# Soft-delete task
@router.delete("/{task_id}", response_model=TaskRead)
async def delete_task(task_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task).where(Task.id == task_id, Task.deleted == False))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(404, "Task not found")
    task.deleted = True
    await session.commit()
    await session.refresh(task)
    return task

# Add comment
@router.post("/{task_id}/comments", response_model=CommentRead)
async def add_comment(task_id: UUID, comment: CommentCreate, session: AsyncSession = Depends(get_session)):
    new_comment = Comment(task_id=task_id, **comment.dict())
    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)
    return new_comment

# Get comments
@router.get("/{task_id}/comments", response_model=list[CommentRead])
async def get_comments(task_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Comment).where(Comment.task_id == task_id))
    return result.scalars().all()