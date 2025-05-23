# Импортируем необходимые библиотеки
from database.models import metadata_obj, users_table, tasks_table, responsible_table, subtask_table, files_table
from database.db import sync_engine
from sqlalchemy import insert, select, update, delete

# Функция создания таблиц
def create_tables():
    # metadata_obj.drop_all(sync_engine)
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
                {"username": username, "userpass": userpass, "permissions": "USER"}
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
def insert_task(title_task):
    with sync_engine.connect() as conn:
        stmt = insert(tasks_table).values(
            {"taskname": title_task, "status": "Выполняется"}
        ).returning(tasks_table.c.id)
        
        result = conn.execute(stmt)
        task_id = result.scalar()
        
        conn.commit()
        return task_id
    
def update_task_status(task_id, new_status):
    with sync_engine.connect() as conn:
        stmt = update(tasks_table).where(tasks_table.c.id == task_id).values(status=new_status)
        conn.execute(stmt)
        conn.commit()

# Функция для записи подзадачи в БД
def insert_subtask(subtask_name, task_id):
    with sync_engine.connect() as conn:
        stmt = insert(subtask_table).values(
            {"subtaskname": subtask_name, "id_task": task_id, "status": "В процессе"}
        ).returning(subtask_table.c.id)
        
        result = conn.execute(stmt)
        subtask_id = result.scalar()
        
        conn.commit()
        return subtask_id

# Функция для записи файла в БД    
def insert_file(task_id, file_name, file_data):
    with sync_engine.connect() as conn:
        stmt = insert(files_table).values(
            id_task=task_id,
            file_name=file_name,
            file_data=file_data
        )
        result = conn.execute(stmt)
        file_id = result.scalar()

        conn.commit()
        return file_id

# Функция находит файл по id
def get_files_by_task(task_id):
    with sync_engine.connect() as conn:
        stmt = select(files_table).where(files_table.c.id_task == task_id)
        result = conn.execute(stmt).fetchall()
        return result

# Функция удаляет файл   
def delete_file(file_id):
    with sync_engine.connect() as conn:
        stmt = delete(files_table).where(files_table.c.id == file_id)
        conn.execute(stmt)
        conn.commit()

# Функция для обновления заголовка задачи    
def update_task(task_id, new_title):
    with sync_engine.connect() as conn:
        stmt = update(tasks_table).where(tasks_table.c.id == task_id).values(taskname=new_title)
        conn.execute(stmt)
        conn.commit()

# Фукнкция для обновления заголовка подзадачи      
def update_subtask(subtask_id, new_title):
    with sync_engine.connect() as conn:
        stmt = update(subtask_table).where(subtask_table.c.id == subtask_id).values(subtaskname=new_title)
        conn.execute(stmt)
        conn.commit()

# Функция обновления статуса подзадачи       
def update_subtask_status(subtask_id, new_status):
    with sync_engine.connect() as conn:
        stmt = update(subtask_table).where(subtask_table.c.id == subtask_id).values(status=new_status)
        conn.execute(stmt)
        conn.commit()

# Функция для удаления задачи       
def delete_task(task_id, task_container, all_task_list, page, dialog):
    with sync_engine.connect() as conn:
        # Удаляем связи с таблицей responsible
        conn.execute(delete(responsible_table).where(responsible_table.c.id_task == task_id))
        conn.execute(delete(subtask_table).where(subtask_table.c.id_task == task_id))
        conn.execute(delete(files_table).where(files_table.c.id_task == task_id))
        
        # Удаляем задачу
        stmt = delete(tasks_table).where(tasks_table.c.id == task_id)
        conn.execute(stmt)
        conn.commit()
    
    # Закрываем диалоговое окно
    dialog.open = False
    page.update()
    
    # Удаляем задачу из списка 
    all_task_list.controls.remove(task_container)
    page.update()

# Функция возвращает True если пользователь администратор       
def get_role_user(login):
    with sync_engine.connect() as conn:
        stmt = select(users_table).where(users_table.c.username == login)
        result = conn.execute(stmt)
        user = result.fetchone()
        
        if user.permissions == "ADMIN":
            return True
        else:
            return False
        
# Функция получения всех пользователей из БД
def get_users():
    with sync_engine.connect() as conn:
        stmt = select(users_table)
        result = conn.execute(stmt)
        return result.fetchall()        

# Функция получения всех задач из БД
def get_tasks():
    with sync_engine.connect() as conn:
        stmt = select(tasks_table)
        result = conn.execute(stmt)
        return result.fetchall()
    
# Функция для получения всех подзадач из БД
def get_subtasks():
    with sync_engine.connect() as conn:
        stmt = select(subtask_table)
        result = conn.execute(stmt)
        return result.fetchall()

# Функция ищет id пользователя по его логину
def get_user_id_by_login(login):
    with sync_engine.connect() as conn:
        stmt = select(users_table).where(users_table.c.username == login)
        result = conn.execute(stmt)
        user = result.fetchone()
        return user.id

# Функция добавляет ответсвенный к задачам    
def insert_person(id_task, id_user):
    with sync_engine.connect() as conn:
        stmt = insert(responsible_table).values(
            {
                "id_task": id_task, "id_user": id_user
            }
        )
        
        conn.execute(stmt)
        conn.commit()
        
# Функция ищет пользователя, который уже связан с задачей
def get_associated_users(task_id):
    with sync_engine.connect() as conn:
        stmt = select(responsible_table.c.id_user).where(responsible_table.c.id_task == task_id)
        result = conn.execute(stmt)
        return [row[0] for row in result]

# Функция удаляет пользователя с задачи
def remove_user_from_task(task_id, user_id):
    with sync_engine.connect() as conn:
        stmt = delete(responsible_table).where(responsible_table.c.id_task == task_id, responsible_table.c.id_user == user_id)
        conn.execute(stmt)
        conn.commit()
    
# Функция ищет исполнителей у задачи
def get_responsible_users(task_id):
    with sync_engine.connect() as conn:
        stmt = select(responsible_table.c.id_user).where(responsible_table.c.id_task == task_id)
        result = conn.execute(stmt)
        return [row[0] for row in result]
        
# Функция считает колличество подзадач 
def get_str_subtasks(task_id):
    with sync_engine.connect() as conn: 
        stmt = select(subtask_table.c.id).where(subtask_table.c.id_task == task_id)
        result = conn.execute(stmt)
        return result 

# Функция обновляет данные пользователя
def update_user(login, new_username, new_password):
    with sync_engine.connect() as conn:
        stmt = update(users_table).where(users_table.c.username == login).values(
            {"username": new_username, "userpass": new_password}
        )
        conn.execute(stmt)
        conn.commit()