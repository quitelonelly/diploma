from sqlalchemy import select

from fastapi import HTTPException

from database.db import new_session
from database.models import responsible_table, subtask_table
from backend.shemas import ResponsibleAdd, Task, TaskAdd, TaskORM, User, UserAdd, UserORM, Subtask, SubtaskAdd, SubtaskORM, UserUpdate

from backend.utils import hash_password, verify_password


class UserRepository:

    @classmethod
    async def add_user(cls, data: UserAdd) -> int:
        async with new_session() as session:
            # Проверяем, существует ли уже пользователь с таким логином
            existing_user = await cls.get_user_by_username(data.username)
            if existing_user:
                raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует")

            user_dict = data.model_dump()
            user_dict['userpass'] = hash_password(data.userpass)  # Хешируем пароль перед сохранением

            user = UserORM(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()

            return user.id
        
    @classmethod
    async def get_users(cls):
        async with new_session() as session:
            query = select(UserORM)
            result = await session.execute(query)
            user_models = result.scalars().all()
            
            user_dicts = [user_models_to_dict(user_model) for user_model in user_models]
            
            user_schemas = [User(**user_dict) for user_dict in user_dicts]
            return user_schemas
        
    @classmethod
    async def update_user(cls, data: UserUpdate) -> bool:
        async with new_session() as session:
            user = await session.get(UserORM, data.id)

            if not user:
                return False  # Пользователь не найден

            # Обновляем только указанные поля
            if data.username is not None:
                user.username = data.username
            if data.userpass is not None:
                user.userpass = data.userpass
            if data.permissions is not None:
                user.permissions = data.permissions

            await session.commit()
            return True
        
    @classmethod
    async def get_user_by_username(cls, username: str):
        async with new_session() as session:
            query = select(UserORM).where(UserORM.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            return user
        
    @classmethod
    async def get_user_role_by_username(cls, username: str):
        async with new_session() as session:
            query = select(UserORM.permissions).where(UserORM.username == username)
            result = await session.execute(query)
            role = result.scalar_one_or_none()

            return role

        
class TaskRepository:
    
    @classmethod
    async def add_task(cls, data: TaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskORM(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()

            return task.id
    
    @classmethod
    async def get_tasks(cls):
        async with new_session() as session:
            query = select(TaskORM)
            result = await session.execute(query)
            task_models = result.scalars().all()

            task_dicts = [task_models_to_dict(task_model) for task_model in task_models]

            task_schemas = [Task(**task_dict) for task_dict in task_dicts]
            return task_schemas
        
    @classmethod
    async def update_task_name(cls, task_id: int, new_name: str) -> bool:
        async with new_session() as session:
            # Получаем задачу по ID
            task = await session.get(TaskORM, task_id)

            if not task:
                return False  # Задача не найдена

            # Обновляем название задачи
            task.taskname = new_name
            await session.commit()  # Сохраняем изменения в базе данных
            return True  # Успешное обновление

    @classmethod
    async def get_tasks_by_user_id(cls, user_id: int):
        async with new_session() as session:
            query = (
                select(TaskORM)
                .join(responsible_table, TaskORM.id == responsible_table.c.id_task)
                .where(responsible_table.c.id_user == user_id)
            )
            result = await session.execute(query)
            task_models = result.scalars().all()

            task_dicts = [task_models_to_dict(task_model) for task_model in task_models]
            
            task_schemas = [Task(**task_dict) for task_dict in task_dicts]
            return task_schemas
        
    @classmethod
    async def add_responsible(cls, data: ResponsibleAdd) -> bool:
        async with new_session() as session:
            try:
                new_responsible = {
                    "id_task": data.task_id,
                    "id_user": data.user_id
                }

                result = await session.execute(responsible_table.insert().values(new_responsible))
                await session.commit()

                if result.rowcount == 0:
                    return False
                
                return True
            except Exception as e:
                return False
            
    @classmethod
    async def delete_responsible(cls, task_id: int, user_id: int) -> bool:
        async with new_session() as session:
            try:
                await session.execute(
                    responsible_table.delete().where(
                        (responsible_table.c.id_task == task_id) &
                        (responsible_table.c.id_user == user_id)
                    )
                )
                await session.commit()
                return True
            except Exception as e:
                return False
            
class SubtaskRepository:

    @classmethod
    async def add_subtask(cls, task_id: int, data: SubtaskAdd) -> int:
        async with new_session() as session:
            subtask_dict = data.model_dump()

            # Связываем подзадачу с задачей
            subtask = SubtaskORM(**subtask_dict, id_task=task_id)
            session.add(subtask)
            await session.flush()
            await session.commit()

            return subtask.id

    @classmethod
    async def get_subtasks(cls, task_id: int):
        async with new_session() as session:
            # Выбираем объекты ORM
            query = select(SubtaskORM).where(SubtaskORM.id_task == task_id)
            result = await session.execute(query)
            subtask_models = result.scalars().all()  # Это должно вернуть объекты ORM

            # Преобразуем объекты ORM в модели ответа
            subtask_responses = [
                Subtask(id=subtask_model.id, subtaskname=subtask_model.subtaskname, status=subtask_model.status)
                for subtask_model in subtask_models
            ]

            return subtask_responses
        
def user_models_to_dict(user_model: UserORM) -> dict:
    return {
        'id': user_model.id,
        'username': user_model.username,
        'userpass': user_model.userpass,  
        'permissions': user_model.permissions 
    }
    
def task_models_to_dict(task_model: TaskORM) -> dict:
    return {
        'id': task_model.id,
        'taskname': task_model.taskname,
        'status': task_model.status,
    }

def subtask_models_to_dict(subtask_model: SubtaskORM) -> dict:
    return {
        'id': subtask_model.id,
        'subtaskname': subtask_model.subtaskname,
        'status': subtask_model.status,
    }