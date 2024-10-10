from sqlalchemy import select
from database.db import new_session
from database.core import UserORM
from backend.shemas import User


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
            
            
def user_models_to_dict(user_model: UserORM) -> dict:
    return {
        'id': user_model.id,
        'name': user_model.username,
        'password': user_model.userpass,  
        'permission': user_model.permissions 
    }