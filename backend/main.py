from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.repository import UserRepository
from backend.shemas import User


app = FastAPI(
    title="Pulse"
)

# Получение всех пользователей приложения
@app.get("/users")
async def get_users() -> list[User]:
    users = await UserRepository.get_users()
    return users
    

# Получение всех задач
@app.get("/tasks")
async def get_tasks():
    ...
    
# Получение задач по пользователю
@app.get("/tasks/{user_id}")
async def get_tasks(user_id: int):
    ...
