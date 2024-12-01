# Импортируем необходимые библиотеки
import flet as ft
import httpx

from database.core import create_tables, insert_user, check_user_pass
from frontend.screen_app import main_screen
from frontend.layout import (
    create_input_login, create_input_pass, create_btn_reg, 
    create_btn_auth, create_sign_in_btn, create_sign_up_button, 
    create_reg_panel, create_auth_panel
                             )

def main(page):
    page.title = "Pulse"
    page.theme_mode = "dark"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 450
    page.window.height = 450
    page.window.resizable = False
    
    # Вызов функции создания таблиц БД
    create_tables()
    
    # Функция проверки заполнения полей
    def validate(e):
        if all([user_login.value, user_pass.value]):
            btn_registered.disabled = False
            btn_auth.disabled = False
        else: 
            btn_registered.disabled = True
            btn_auth.disabled = True
        page.update()
    
    # Функция закрытия диалогового окна
    def close_dialog(e):
        page.dialog.open = False
        page.update()

    # Функция регистрации
    async def register(e):
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/users", json={
                "username": user_login.value,
                "userpass": user_pass.value,
                "permissions": "USER"
            })
            
            if response.status_code == 200:
                # Успешная регистрация
                page.window.width = 1300
                page.window.height = 750
                page.window.resizable = False
                
                page.clean()
                main_screen(page, user_login.value, user_pass.value) 
                page.update()
                return

            # Обработка ошибок
            if response.status_code == 400:
                dialog = ft.AlertDialog(
                    title=ft.Text("Ошибка"),
                    content=ft.Text(response.json().get("message", "Ошибка")),
                    actions=[ft.TextButton("ОК", on_click=close_dialog)]
                )
                page.dialog = dialog
                dialog.open = True
                
                # Очистка полей после ошибки
                user_login.value = ""
                user_pass.value = ""
                page.update()

    # Функция авторизации            
    async def auth(e):
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/token", data={
                "username": user_login.value,
                "password": user_pass.value
            })
            
            if response.status_code == 200:
                token = response.json().get("access_token")
                # Сохраните токен для дальнейшего использования
                print(f"Получен токен: {token}")  # Для отладки, вы можете сохранить токен в переменной

                # Переход на главный экран
                page.window.width = 1300
                page.window.height = 750
                page.window.resizable = False
                
                page.clean()
                main_screen(page, user_login.value, user_pass.value, token)  # Передаем токен на главный экран
                page.update()
                return

            if response.status_code == 401:
                dialog = ft.AlertDialog(
                    title=ft.Text("Ошибка"),
                    content=ft.Text("Неверные учетные данные!"),
                    actions=[ft.TextButton("OK", on_click=close_dialog)]
                )
                page.dialog = dialog
                dialog.open = True
                
                # Очистка полей после ошибки
                user_login.value = ""
                user_pass.value = ""
                page.update()


    # Функция показывает экран регистрации
    def show_sign_up():
        page.clean()
        page.add(panel_register)

    # Функция показывает экран авторизации
    def show_sign_in():
        page.clean()
        page.add(panel_auth)

    # Поля ввода логина и пароля
    user_login = create_input_login(validate)
    user_pass = create_input_pass(validate)

    # Кнопка регистрации
    btn_registered = create_btn_reg(register)
    # Кнопка авторизации
    btn_auth = create_btn_auth(auth)

    # Кнопка перехода между экранами авторизации и регистрации
    already_registered_text = ft.Text("Уже зарегистрировались?")
    sign_in_button = create_sign_in_btn(show_sign_in)
    
    # Кнопка перехода между экранами авторизации и регистрации
    already_auth_text = ft.Text("Еще не зарегистрировались?")
    sign_up_button = create_sign_up_button(show_sign_up)

    # Экран регистрации
    panel_register = create_reg_panel(user_login, user_pass, btn_registered, already_registered_text, sign_in_button)
    
    # Экран авторизации
    panel_auth = create_auth_panel(user_login, user_pass, btn_auth, already_auth_text, sign_up_button)

    # Показ экрана регистрации
    page.add(panel_auth)

ft.app(target=main)
