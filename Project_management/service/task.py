from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate


# ── CREATE ───────────────────────────────────────────────────────────────────
def create_task(db: Session, task_data: TaskCreate):
    new_task = Task(**task_data.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# ── READ ALL ─────────────────────────────────────────────────────────────────
def get_all_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Task).offset(skip).limit(limit).all()


# ── READ ONE ─────────────────────────────────────────────────────────────────
def get_task_by_id(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return task


# ── READ BY PROJECT ──────────────────────────────────────────────────────────
def get_tasks_by_project(db: Session, project_id: int):
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No tasks found for project {project_id}"
        )
    return tasks


# ── READ BY USER ─────────────────────────────────────────────────────────────
def get_tasks_by_user(db: Session, user_id: int):
    tasks = db.query(Task).filter(Task.assigned_to == user_id).all()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No tasks found for user {user_id}"
        )
    return tasks


# ── UPDATE ───────────────────────────────────────────────────────────────────
def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


# ── DELETE ───────────────────────────────────────────────────────────────────
def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    db.delete(task)
    db.commit()
    return task