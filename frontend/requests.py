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
