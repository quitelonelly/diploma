from sqlalchemy import select
from database.db import new_session
from database.core import UserORM, TaskORM
from database.models import responsible_table
from backend.shemas import Task, User


class UserRepository:
    
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
            
def user_models_to_dict(user_model: UserORM) -> dict:
    return {
        'id': user_model.id,
        'name': user_model.username,
        'password': user_model.userpass,  
        'permission': user_model.permissions 
    }
    
def task_models_to_dict(task_model: TaskORM) -> dict:
    return {
        'id': task_model.id,
        'taskname': task_model.taskname,
    }