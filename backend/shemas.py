from pydantic import BaseModel

class UserAdd(BaseModel):
    name: str
    password: str
    permission: str | None

class User(UserAdd):
    id: int
    
    class Config:
        orm_mode = True