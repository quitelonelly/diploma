import flet as ft

from database.core import create_tables, insert_user, check_user_pass

def main(page):
    page.title = "Flet App"
    page.theme_mode = "dark"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 350
    page.window_height = 450
    page.window_resizable = False
    
    create_tables()
    
    def validate(e):
        if all([user_login.value, user_pass.value]):
            btn_registered.disabled = False
            btn_auth.disabled = False
        else: 
            btn_registered.disabled = True
            btn_auth.disabled = True
        page.update()
    
    def close_dialog(e):
        page.dialog.open = False
        page.update()
    
    def register(e):
        result = insert_user(user_login.value, user_pass.value)

        if result is None:
            dialog = ft.AlertDialog(
                title=ft.Text("Успешно"),
                content=ft.Text("Вы успешно зарегистрировались!"),
                actions=[ft.TextButton("OK", on_click=close_dialog)]
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
            return

        if "существует" in result:
            dialog = ft.AlertDialog(
                title=ft.Text("Ошибка регистрации"),
                content=ft.Text(result),
                actions=[ft.TextButton("OK", on_click=close_dialog)]
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
            
    def auth(e):
        result = check_user_pass(user_login.value, user_pass.value)
        
        if result == True:
            dialog = ft.AlertDialog(
                title=ft.Text("Успешно"),
                content=ft.Text("Вы успешно вошли в систему!"),
                actions=[ft.TextButton("OK", on_click=close_dialog)]
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
            return

        if result == False:
            dialog = ft.AlertDialog(
                title=ft.Text("Ошибка входа"),
                content=ft.Text("Проверьте введенные данные!"),
                actions=[ft.TextButton("OK", on_click=close_dialog)]
            )
            page.dialog = dialog
            dialog.open = True
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
    user_login = ft.TextField(label="Login", width=200, on_change=validate)
    user_pass = ft.TextField(label="Password", width=200, on_change=validate, password=True)

    # Кнопка регистрации
    btn_registered = ft.CupertinoFilledButton(text="Register", width=200, height=50, on_click=register, disabled=True)
    # Кнопка авторизации
    btn_auth = ft.CupertinoFilledButton(text="Entrance", width=200, height=50, on_click=auth, disabled=True)

    # Кнопка перехода между экранами авторизации и регистрации
    already_registered_text = ft.Text("Already registered?")
    sign_in_button = ft.TextButton("Sign In", on_click=lambda e: show_sign_in(), style=ft.ButtonStyle(color=ft.colors.BLUE))
    
    # Кнопка перехода между экранами авторизации и регистрации
    already_auth_text = ft.Text("Not registered yet?")
    sign_up_button = ft.TextButton("Sign Up", on_click=lambda e: show_sign_up(), style=ft.ButtonStyle(color=ft.colors.BLUE))

    # Экран регистрации
    panel_register = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Registered"),
                    user_login,
                    user_pass,
                    btn_registered,
                    ft.Container(
                        content=ft.Column(
                            [
                                already_registered_text,
                                sign_in_button,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.only(left=35),
                    ),
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    # Экран авторизации
    panel_auth = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Entrance"),
                    user_login,
                    user_pass,
                    btn_auth,
                    ft.Container(
                        content=ft.Column(
                            [
                                already_auth_text,
                                sign_up_button,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.only(left=35),
                    ),
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Показ экрана регистрации
    page.add(panel_register)

ft.app(target=main)
