from pydantic import BaseModel

class UserAdd(BaseModel):
    name: str
    password: str
    permission: str | None

class User(UserAdd):
    id: int

        
class TaskAdd(BaseModel):
    taskname: str
    
class Task(TaskAdd):
    id: int