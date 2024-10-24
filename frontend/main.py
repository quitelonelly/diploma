import flet as ft

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
    page.window_width = 400
    page.window_height = 450
    page.window_resizable = False
    
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
    def register(e):
        result = insert_user(user_login.value, user_pass.value)

        if result is None:
            
            page.window_width = 1300
            page.window_height = 750
            page.window_resizable = False
            
            page.clean()
            main_screen(page, user_login.value, user_pass.value) 
            page.update()
            return

        if "существует" in result:
            dialog = ft.AlertDialog(
                title=ft.Text("Ошибка"),
                content=ft.Text(result),
                actions=[ft.TextButton("ОК", on_click=close_dialog)]
            )
            page.dialog = dialog
            dialog.open = True
            
            # Очистка полей после ошибки
            user_login.value = ""
            user_pass.value = ""
            page.update()
    
    # Функция авторизации       
    def auth(e):
        result = check_user_pass(user_login.value, user_pass.value)
        
        if result == True:
            
            page.window_width = 1300
            page.window_height = 750
            page.window_resizable = False
            
            page.clean()
            main_screen(page, user_login.value, user_pass.value) 
            page.update()
            return

        if result == False:
            dialog = ft.AlertDialog(
                title=ft.Text("Ошибка"),
                content=ft.Text("Проверьте введенные данные!"),
                actions=[ft.TextButton("OK", on_click=close_dialog)]
            )
            page.dialog = dialog
            dialog.open = True
            
            # Очистка полей после ошибки
            create_input_login(validate).value = ""
            create_input_pass(validate).value = ""
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
    page.add(panel_register)

ft.app(target=main)
