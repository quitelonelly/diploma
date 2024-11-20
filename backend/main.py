from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from backend.repository import TaskRepository, UserRepository, SubtaskRepository
from backend.shemas import Task, TaskAdd, User, UserAdd, Subtask, SubtaskAdd


app = FastAPI(
    title="Pulse"
)

# Запись нового пользователя в БД
@app.post("/new_user")
async def add_user(user: Annotated[UserAdd, Depends()]) -> JSONResponse:
    user_id = await UserRepository.add_user(user)
    return {"User added": True, "user_id": user_id}

# Получение всех пользователей приложения
@app.get("/users")
async def get_users() -> list[User]:
    users = await UserRepository.get_users()
    return users

# Запись новой задачи в БД
@app.post("/new_task")
async def add_task(task: Annotated[TaskAdd, Depends()]) -> JSONResponse:
    task_id = await TaskRepository.add_task(task)
    return {"Task added": True, "task_id": task_id}

# Получение всех задач
@app.get("/tasks")
async def get_tasks() -> list[Task]:
    tasks = await TaskRepository.get_tasks()
    return tasks
    
# Получение задач по пользователю
@app.get("/tasks/{user_id}")
async def get_tasks_by_user_id(user_id: int) -> list[Task]:
    tasks = await TaskRepository.get_tasks_by_user_id(user_id)
    return tasks

# Получение подзадач по задаче
@app.get("/subtasks/{task_id}")
async def get_subtasks_by_task_id(task_id: int) -> list[Subtask]:
    subtasks = await SubtaskRepository.get_subtasks(task_id)
    return subtasks
