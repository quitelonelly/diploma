from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Model(DeclarativeBase):
    pass


class UserAdd(BaseModel):
    username: str
    userpass: str
    permissions: str | None


class UserORM(Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    userpass: Mapped[str]
    permissions: Mapped[str | None]


class UserUpdate(BaseModel):
    id: int
    username: str | None
    userpass: str | None
    permissions: str | None


class User(UserAdd):
    id: int


class TaskAdd(BaseModel):
    taskname: str


class TaskORM(Model):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    taskname: Mapped[str]
    status: Mapped[str] = mapped_column(default="Выполняется")

    
class Task(TaskAdd):
    status: str
    id: int


class ResponsibleAdd(BaseModel):
    task_id: int
    user_id: int


class SubtaskAdd(BaseModel):
    subtaskname: str
    

class SubtaskORM(Model):
    __tablename__ = "subtasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_task: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    subtaskname: Mapped[str]
    status: Mapped[str] = mapped_column(default="В процессе")


class Subtask(SubtaskAdd):
    status: str
    id: int