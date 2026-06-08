from database.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
import enum


class TaskStatus(str, enum.Enum):
    pending    = "pending"
    inprogress = "inprogress"
    completed  = "completed"


class Task(Base):
    __tablename__ = "tasks"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    status      = Column(Enum(TaskStatus), default=TaskStatus.pending, nullable=False)
    project_id  = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=False)
    due_date    = Column(DateTime(timezone=True), nullable=True)
