import flet as ft

from database.core import create_tables, insert_user

def main(page):
    page.title = "Flet App"
    page.theme_mode = "dark" # light
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 350
    page.window_height = 400
    page.window_resizable = False
    
    create_tables()
    
    # Проверка заполнения всех полей
    def validate(e):
        if all([user_login.value, user_pass.value]):
            btn_registered.disabled = False
        else: 
            btn_registered.disabled = True
            
        page.update()
    
     # Функция для закрытия диалогового окна
    def close_dialog(e):
        page.dialog.open = False
        page.update()
    
    # Функция регистрации
    def register(e):
        result = insert_user(user_login.value, user_pass.value)

        # Проверяем, что результат не None
        if result is None:
            dialog = ft.AlertDialog(
                title=ft.Text("Ошибка"),
                content=ft.Text("Произошла ошибка при регистрации."),
                actions=[ft.TextButton("OK", on_click=close_dialog)]
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
            return

        # Если пользователь уже существует, показываем окно с сообщением
        if "существует" in result:
            dialog = ft.AlertDialog(
                title=ft.Text("Ошибка регистрации"),
                content=ft.Text(result),
                actions=[ft.TextButton("OK", on_click=close_dialog)]
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
        else:
            ...
    
    user_login = ft.TextField(label="Login", width=200, on_change=validate)
    user_pass = ft.TextField(label="Password", width=200, on_change=validate)
    btn_registered = ft.OutlinedButton(text="Register", width=200, on_click=register, disabled=True)
    
    # Дизайн экрана регистрации    
    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Registration"),
                        
                        user_login,
                        user_pass,
                        btn_registered
                    ]
                )
            ],
            alignment = ft.MainAxisAlignment.CENTER
        )
    )
    
    
ft.app(target=main)