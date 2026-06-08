from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.project import Project
from schemas.project import ProjectCreate, ProjectUpdate
from models.task import Task



# ── CREATE ───────────────────────────────────────────────────────────────────
def create_project(db: Session, project_data: ProjectCreate):
    new_project = Project(**project_data.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


# ── READ ALL ─────────────────────────────────────────────────────────────────
def get_all_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Project).offset(skip).limit(limit).all()


# ── READ ONE ─────────────────────────────────────────────────────────────────
def get_project_by_id(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found"
        )
    return project


# ── READ BY MANAGER ──────────────────────────────────────────────────────────
def get_projects_by_manager(db: Session, user_id: int):
    projects = db.query(Project).filter(Project.created_by == user_id).all()
    if not projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No projects found for manager {user_id}"
        )
    return projects


# ── UPDATE ───────────────────────────────────────────────────────────────────
def update_project(db: Session, project_id: int, project_data: ProjectUpdate):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found"
        )
    for key, value in project_data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project


# ── DELETE ───────────────────────────────────────────────────────────────────
def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found"
        )
    db.delete(project)
    db.commit()
    return project


def get_projects_by_user(
    db: Session,
    user_id: int
):
    projects = (
        db.query(Project)
        .join(Task, Task.project_id == Project.id)
        .filter(Task.assigned_to == user_id)
        .distinct()
        .all()
    )

    return projects