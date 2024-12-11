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
      
async def request_get_user_role(user_login):
      async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/users/role", params={
                "username": user_login,
            })

            return response
      
async def request_confirm_name_task(task_id, title_task):
      async with httpx.AsyncClient() as client:
            response = await client.put(f"http://localhost:8000/tasks/{task_id}/name", params={
                "new_name": title_task,
                })
            
            return response