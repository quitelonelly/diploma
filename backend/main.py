import os

from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, Security, Body
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend.repository import TaskRepository, UserRepository, SubtaskRepository
from backend.shemas import ResponsibleAdd, Task, TaskAdd, User, UserAdd, Subtask, SubtaskAdd, UserUpdate
from backend.utils import hash_password, verify_password


app = FastAPI(
    title="Pulse"
)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Инициализация хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Инициализация OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Функция для создания токена
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# Функция для получения текущего пользователя
async def get_current_user(token: str = Security(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id  # Возвращаем ID пользователя
    except JWTError:
        raise credentials_exception
    
@app.post("/token", tags=["Аутентификация"], summary="Получить токен доступа")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    user = await UserRepository.get_user_by_username(form_data.username)  # Создайте этот метод в UserRepository
    if not user or not verify_password(form_data.password, user.userpass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Запись нового пользователя
@app.post("/users", tags=["Пользователи 👤"], summary="Добавить нового пользователя")
async def add_user(user: Annotated[UserAdd, Depends()]) -> JSONResponse:
    user_id = await UserRepository.add_user(user)

    # Создаем токен для нового пользователя
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user_id}, expires_delta=access_token_expires)

    return {"User  added": True, "user_id": user_id, "access_token": access_token, "token_type": "bearer"}

# Получение всех пользователей приложения
@app.get("/users", tags=["Пользователи 👤"], summary="Получить всех пользователей")
async def get_users() -> list[User]:
    users = await UserRepository.get_users()
    return users

# Получение роли пользователя
@app.get("/users/role", tags=["Пользователи 👤"], summary="Получить роль пользователя")
async def get_user_role_by_username(username: str) -> str:
    role = await UserRepository.get_user_role_by_username(username)
    return role

# Обновление пользователя
@app.put("/users", tags=["Пользователи 👤"], summary="Обновить данные пользователя")
async def update_user(user: Annotated[UserUpdate, Depends()]) -> JSONResponse:
    updated = await UserRepository.update_user(user)
    if updated:
        return {"User updated": True}
    return JSONResponse(status_code=404, content={"message": "User not found"})


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

@app.delete("/tasks/{task_id}", tags=["Задачи 📝"], summary="Удалить задачу")
async def delete_task(task_id: int) -> JSONResponse:
    deleted = await TaskRepository.delete_task(task_id)
    if deleted:
        return {"message": "Task deleted successfully"}
    return JSONResponse(status_code=404, content={"message": "Task not found"})
    
# Получение задач по пользователю
@app.get("/tasks/{user_id}", tags=["Задачи 📝"], summary="Получить задачи по пользователю")
async def get_tasks_by_user_id(user_id: int) -> list[Task]:
    tasks = await TaskRepository.get_tasks_by_user_id(user_id)
    return tasks

# Запись ответственного за задачу
@app.post("/tasks/responsibles", tags=["Задачи 📝"], summary="Добавить ответственного за задачу")
async def assign_responsible(responsible: Annotated[ResponsibleAdd, Depends()]) -> JSONResponse:
    try:
        success = await TaskRepository.add_responsible(responsible)
        if success:
            return {"message": "Responsible assigned successfully"}
        return JSONResponse(status_code=400, content={"message": "Failed to assign responsible"})
    except Exception as e:
        print(f"Ошибка при добавлении исполнителя: {e}")  # Логируем ошибку
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
    
# Удаление ответственного за задачу
@app.delete("/tasks/responsibles/{task_id}/{user_id}", tags=["Задачи 📝"], summary="Удалить ответственного за задачу")
async def remove_responsible(task_id: int, user_id: int) -> JSONResponse:
    print(f"Удаление исполнителя: task_id={task_id}, user_id={user_id}")
    try:
        success = await TaskRepository.delete_responsible(task_id, user_id)
        if success:
            return {"message": "Responsible removed successfully"}
        return JSONResponse(status_code=404, content={"message": "Failed to remove responsible"})
    except Exception as e:
        print(f"Ошибка при удалении исполнителя: {e}")  # Логируем ошибку
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

# Обновление названия задачи
@app.put("/tasks/{task_id}/name", tags=["Задачи 📝"], summary="Обновить название задачи")
async def update_task_name(task_id: int, new_name: str) -> JSONResponse:
    updated = await TaskRepository.update_task_name(task_id, new_name)
    if updated:
        return {"message": "Task name updated successfully"}
    return JSONResponse(status_code=404, content={"message": "Task not found"})

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

# Обновление статуса подзадачи
@app.put("/subtasks/{subtask_id}/status", tags=["Задачи 📝"], summary="Обновить статус подзадачи")
async def update_subtask_status(subtask_id: int, new_status: str) -> JSONResponse:
    updated = await SubtaskRepository.update_subtask_status(subtask_id, new_status)
    if updated:
        return {"message": "Subtask status updated successfully"}
    return JSONResponse(status_code=404, content={"message": "Subtask not found"})
