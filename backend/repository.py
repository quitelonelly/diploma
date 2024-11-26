from sqlalchemy import select
from database.db import new_session
from database.models import responsible_table, subtask_table
from backend.shemas import Task, TaskAdd, TaskORM, User, UserAdd, UserORM, Subtask, SubtaskAdd, SubtaskORM


class UserRepository:

    @classmethod
    async def add_user(cls, data: UserAdd) -> int:
        async with new_session() as session:
            user_dict = data.model_dump()

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