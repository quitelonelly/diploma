from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from backend.repository import TaskRepository, UserRepository, SubtaskRepository
from backend.shemas import ResponsibleAdd, Task, TaskAdd, User, UserAdd, Subtask, SubtaskAdd, UserUpdate


app = FastAPI(
    title="Pulse"
)

# Запись нового пользователя
@app.post("/users", tags=["Пользователи 👤"], summary="Добавить нового пользователя")
async def add_user(user: UserAdd) -> JSONResponse:
    print(user) 
    user_id = await UserRepository.add_user(user)
    return {"User added": True, "user_id": user_id}

# Получение всех пользователей приложения
@app.get("/users", tags=["Пользователи 👤"], summary="Получить всех пользователей")
async def get_users() -> list[User]:
    users = await UserRepository.get_users()
    return users

# Обновление пользователя
@app.put("/users", tags=["Пользователи 👤"], summary="Обновить данные пользователя")
async def update_user(user: Annotated[UserUpdate, Depends()]) -> JSONResponse:
    updated = await UserRepository.update_user(user)
    if updated:
        return {"User  updated": True}
    return JSONResponse(status_code=404, content={"message": "User  not found"})

# Запись новой задачи
@app.post("/tasks", tags=["Задачи 📝"], summary="Добавить новую задачу")
async def add_task(task: Annotated[TaskAdd, Depends()]) -> JSONResponse:
    task_id = await TaskRepository.add_task(task)
    return {"Task added": True, "task_id": task_id}

# Получение всех задач
@app.get("/tasks", tags=["Задачи 📝"], summary="Получить все задачи")
async def get_tasks() -> list[Task]:
    tasks = await TaskRepository.get_tasks()
    return tasks
    
# Получение задач по пользователю
@app.get("/tasks/{user_id}", tags=["Задачи 📝"], summary="Получить задачи по пользователю")
async def get_tasks_by_user_id(user_id: int) -> list[Task]:
    tasks = await TaskRepository.get_tasks_by_user_id(user_id)
    return tasks

# Запись ответственного за задачу
@app.post("/tasks/responsibles", tags=["Задачи 📝"], summary="Добавить ответственного за задачу")
async def assign_responsible(responsible: Annotated[ResponsibleAdd, Depends()]) -> JSONResponse:
    success = await TaskRepository.add_responsible(responsible)
    if success:
        return {"message": "Responsible assigned successfully"}
    return JSONResponse(status_code=400, content={"message": "Failed to assign responsible"})

# Запись новой подзадачи
@app.post("/subtasks/{task_id}", tags=["Задачи 📝"], summary="Добавить новую подзадачу")
async def add_subtask(task_id: int, subtask: Annotated[SubtaskAdd, Depends()]) -> JSONResponse:
    subtask_id = await SubtaskRepository.add_subtask(task_id, subtask)
    return {"Subtask added": True, "subtask_id": subtask_id}

# Получение подзадач по задаче
@app.get("/subtasks/{task_id}", tags=["Задачи 📝"], summary="Получить подзадачи по задаче")
async def get_subtasks_by_task_id(task_id: int) -> list[Subtask]:
    subtasks = await SubtaskRepository.get_subtasks(task_id)
    return subtasks
