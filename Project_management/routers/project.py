from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from service.projects import (
    create_project,
    get_all_projects,
    get_project_by_id,
    update_project,
    delete_project,
    get_projects_by_user
)

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, status_code=201)
def create(payload: ProjectCreate, db: Session = Depends(get_db)):
    return create_project(db, payload)


@router.get("/", response_model=List[ProjectResponse])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_projects(db, skip, limit)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_one(project_id: int, db: Session = Depends(get_db)):
    return get_project_by_id(db, project_id)


@router.put("/{project_id}", response_model=ProjectResponse)
def update(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    return update_project(db, project_id, payload)


@router.delete("/{project_id}", status_code=204)
def delete(project_id: int, db: Session = Depends(get_db)):
    return delete_project(db, project_id)

@router.get("/{user_id}")
def get_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_projects_by_user(
        db,
        user_id
    )