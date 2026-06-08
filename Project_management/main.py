from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware


from routers.users import router as user_router
from routers.project import router as project_router
from routers.task import router as task_router
from routers.auth import router as auth_router

from database.database import Base, engine

from models.user import customuser
from models.project import Project
from models.task import Task

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Project Management ")

app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(auth_router)





app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)