from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.repository import TaskRepository, UserRepository
from backend.shemas import Task, User


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
async def get_tasks() -> list[Task]:
    tasks = await TaskRepository.get_tasks()
    return tasks
    
# Получение задач по пользователю
@app.get("/tasks/{user_id}")
async def get_tasks_by_user_id(user_id: int):
    tasks = await TaskRepository.get_tasks_by_user_id(user_id)
    return tasks
