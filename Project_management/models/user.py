from sqlalchemy import Column, Integer, String, Enum
from database.database import Base
import enum



class UserRole(str, enum.Enum):
    admin = "admin"           
    developer = "developer" 

class customuser(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(255), unique=True, nullable=False, index=True)
    password   = Column(String(255), nullable=False)
    role       = Column(Enum(UserRole), default=UserRole.developer, nullable=False)
