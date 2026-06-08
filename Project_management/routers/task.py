from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from service.task import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    get_tasks_by_project,
    get_tasks_by_user,
    update_task,
    delete_task
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create(payload: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, payload)


@router.get("/", response_model=List[TaskResponse])
def get_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_tasks(db, skip, limit)


@router.get("/project/{project_id}", response_model=List[TaskResponse])
def get_by_project(project_id: int, db: Session = Depends(get_db)):
    return get_tasks_by_project(db, project_id)


@router.get("/{user_id}", response_model=List[TaskResponse])
def get_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_tasks_by_user(db, user_id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_one(task_id: int, db: Session = Depends(get_db)):
    return get_task_by_id(db, task_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    return update_task(db, task_id, payload)


@router.delete("/{task_id}", status_code=204)
def delete(task_id: int, db: Session = Depends(get_db)):
    return delete_task(db, task_id)