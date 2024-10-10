from typing import Annotated
from fastapi import APIRouter, Depends

from backend.repository import UserRepository
from backend.shemas import UserAdd, User

router = APIRouter(
    prefix="/pulse"
)

# Получение всех пользователей приложения
@router.get("/users")
async def get_users() -> list[User]:
    users = await UserRepository.get_users()
    return users
    

# Получение всех задач
@router.get("/tasks")
async def get_tasks():
    ...
    
# Получение задач по пользователю
@router.get("/tasks/{user_id}")
async def get_tasks(user_id: int):
    ...