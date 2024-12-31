from fastapi import UploadFile
import httpx

async def request_reg(user_login, user_pass):
    async with httpx.AsyncClient() as client:
            username = user_login
            userpass = user_pass
            permissions = "USER"

            print(f"Username: {username}, Userpass: {userpass}, Permissions: {permissions}")

            response = await client.post("http://localhost:8000/users", params={
                "username": username,
                "userpass": userpass,
                "permissions": permissions
            })

            return response
    
async def request_auth(user_login, user_pass):
      async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/token", data={
                "username": user_login,
                "password": user_pass
            })

            return response
      
async def request_get_users():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/users")
        if response.status_code == 200:
            return response.json()  # Извлекаем JSON-данные из ответа
        else:
            print(f"Ошибка при получении пользователей: {response.status_code}, {response.text}")
            return []  # Возвращаем пустой список в случае ошибки
      
async def request_get_user_role(user_login):
      async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/users/role", params={
                "username": user_login,
            })

            return response
      
async def request_add_task(taskname):
      async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/tasks", params={
                  "taskname": taskname
            })

            return response
      
async def request_confirm_name_task(task_id, title_task):
      async with httpx.AsyncClient() as client:
            response = await client.put(f"http://localhost:8000/tasks/{task_id}/name", params={
                "new_name": title_task,
                })
            
            return response
      
async def request_get_tasks():
      async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/tasks")

            return response
    
async def request_delete_task(task_id, task_container, all_task_list, page, dialog):
     async with httpx.AsyncClient() as client:
            response = await client.delete(f"http://localhost:8000/tasks/{task_id}")

            # Закрываем диалоговое окно
            dialog.open = False
            page.update()
            
            # Удаляем задачу из списка 
            all_task_list.controls.remove(task_container)
            page.update()

            return response
      
async def request_get_my_tasks(user_id: int):
      async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8000/tasks/{user_id}")

            return response
      
async def request_add_subtask(task_id: int, subtask_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:8000/subtasks/{task_id}", params={
            "subtaskname": subtask_name
        })

        return response
      
async def request_get_subtasks(task_id: int):
      async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8000/subtasks/{task_id}")

      return response

async def request_update_subtask_status(subtask_id: int, status: str):
      async with httpx.AsyncClient() as client:
            response = await client.put(f"http://localhost:8000/subtasks/{subtask_id}/status", params={
                "new_status": status
            })

            return response

async def request_add_responsible(task_id: int, user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/tasks/responsibles", params={
            "task_id": task_id,
            "user_id": user_id 
        })

        return response
    
async def request_delete_responsible(task_id: int, user_id: int):
     async with httpx.AsyncClient() as client:
            response = await client.delete(f"http://localhost:8000/tasks/responsibles/{task_id}/{user_id}")

            return response
     
async def request_add_file(task_id: int, file_name: str, file_data: bytes):
    async with httpx.AsyncClient() as client:
        # Используем multipart/form-data для загрузки файла
        files = {'file': (file_name, file_data, 'application/octet-stream')}
        response = await client.post("http://localhost:8000/files", files=files, data={"task_id": task_id})

        return response
    
async def request_get_files_by_task_id(task_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/tasks/{task_id}/files")
        
        if response.status_code == 200:
            return response.json()  # Возвращаем JSON-данные, если запрос успешен
        else:
            print(f"Ошибка при получении файлов: {response.status_code}, {response.text}")
            return []  # Возвращаем пустой список в случае ошибки
        
async def request_get_file(file_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"http://localhost:8000/files/{file_id}")

            # Проверяем статус ответа
            response.raise_for_status()  # Это вызовет исключение для статусов 4xx и 5xx

            return response.content  # Возвращаем содержимое файла, если запрос успешен
        except httpx.HTTPStatusError as e:
            print(f"Ошибка при получении файла: {e.response.status_code}, {e.response.text}")
            return None  # Возвращаем None в случае ошибки
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            return None  # Возвращаем None в случае других ошибок
        
async def request_delete_file(file_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"http://localhost:8000/files/{file_id}")

        return response