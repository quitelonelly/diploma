from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Model(DeclarativeBase):
    pass

class UserORM(Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    userpass: Mapped[str]
    permissions: Mapped[str | None]

class TaskORM(Model):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    taskname: Mapped[str]
    

class UserAdd(BaseModel):
    username: str
    userpass: str
    permissions: str | None

class User(UserAdd):
    id: int

        
class TaskAdd(BaseModel):
    taskname: str
    
class Task(TaskAdd):
    id: int