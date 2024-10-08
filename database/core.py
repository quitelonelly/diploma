from database.models import metadata_obj, users_table, tasks_table
from database.db import sync_engine
from sqlalchemy import insert, select, update

# Функция создания таблиц
def create_tables():
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    
# Функция добавления пользователя в БД
def insert_user(username, userpass):
    # Проверяем, существует ли пользователь в БД
    if check_user(username):
        return f"Пользователь с именем {username} уже существует!"
    
    with sync_engine.connect() as conn:
        # Если пользователь не найден, добавляем новые данные
        stmt = insert(users_table).values(
            [
                {"username": username, "userpass": userpass}
            ]
        )
        conn.execute(stmt)
        conn.commit()
    
# Функция проверки, есть ли пользователь в БД
def check_user(username):
    
    with sync_engine.connect() as conn:
        stmt = select(users_table).where(users_table.c.username == username)
        result = conn.execute(stmt).fetchone()
        
        if result:
            return True
        else:
            return False

# Функция проверки, логина и пароля пользователя       
def check_user_pass(username, userpass):
    
    with sync_engine.connect() as conn:
        stmt = select(users_table).where(users_table.c.username == username, users_table.c.userpass == userpass)
        result = conn.execute(stmt).fetchone()
        
        if result:
            return True
        else:
            return False
        
# Функция для записи задачи в БД
def insert_task(title_task, user_id):
    with sync_engine.connect() as conn:
        stmt = insert(tasks_table).values(
            {"id_user": user_id, "taskname": title_task}
        ).returning(tasks_table.c.id)
        result = conn.execute(stmt)
        task_id = result.scalar()
        conn.commit()
        return task_id
    
def update_task(task_id, new_title):
    with sync_engine.connect() as conn:
        stmt = update(tasks_table).where(tasks_table.c.id == task_id).values(taskname=new_title)
        conn.execute(stmt)
        conn.commit()
        
# Функция ищет id пользователя по его логину
def get_user_id_by_login(login):
    with sync_engine.connect() as conn:
        stmt = select(users_table).where(users_table.c.username == login)
        result = conn.execute(stmt)
        user = result.fetchone()
        return user.id