from database.database import Base
from sqlalchemy import Column ,Integer,String,DateTime
from sqlalchemy.sql import func


class  Project(Base):
    __tablename__ ="projects"
    
    
    id  = Column(Integer,primary_key=True)
    name =Column(String(100),nullable=False)
    description=Column(String(250),nullable=True)
    created_by=Column(Integer, nullable=False) 