import threading
import flet as ft
import time

def main_screen(page, login, password):
    
    # Создаем кнопку "Личный кабинет"
    account_button = ft.Row(
        [
            ft.Icon(ft.icons.ACCOUNT_CIRCLE, color=ft.colors.WHITE),
            ft.Text("Личный кабинет", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
            ft.Icon(ft.icons.ARROW_DROP_DOWN, color=ft.colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Маскируем пароль звёздочками
    masked_password = "*" * len(password)

    login_tile_container = ft.Container(
        content=ft.ListTile(
            title=ft.Text(login, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=24),
            subtitle=ft.Text("Ваш логин", color=ft.colors.WHITE70),
        ),
    )

    # Отображаем пароль как звёздочки
    password_tile_container = ft.Container(
        content=ft.ListTile(
            title=ft.Text(masked_password, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=22),
            subtitle=ft.Text("Ваш пароль", color=ft.colors.WHITE70),
        ),
    )

    # Создаем кнопку "Редактировать" с другим стилем
    edit_button = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.icons.SETTINGS, color=ft.colors.WHITE, size=20),
                ft.Text("Редактировать", color=ft.colors.WHITE, size=20),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        height=50,
        bgcolor="#ff9800",  # Оранжевый фон
        border_radius=ft.border_radius.all(10),  # Закругленные углы
        padding=ft.padding.all(10),
        expand=True
    )

    # Создаем кнопку "Выйти" с другим стилем
    exit_button = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.icons.EXIT_TO_APP, color=ft.colors.WHITE, size=20),
                ft.Text("Выйти", color=ft.colors.WHITE, size=20),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        height=50,
        bgcolor="#f44336",  # Красный фон
        border_radius=ft.border_radius.all(10),  # Закругленные углы
        padding=ft.padding.all(10),
        expand=True
    )

    # Функции кнопок "Редактировать" и "Выйти"
    def edit_profile(e):
        print("Редактирование профиля")

    def exit_profile(e):
        print("Выход из профиля")
        
    # Создаем контент для окна "Личный кабинет"
    def show_profile_dialog(e):
        def close_dialog(dialog):
            dialog.open = False
            page.update()

        close_icon = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_color=ft.colors.WHITE,
            on_click=lambda _: close_dialog(profile_dialog)
        )

        profile_dialog = ft.AlertDialog(
            modal=False,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [close_icon],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        login_tile_container,
                        password_tile_container,
                        ft.Container(content=edit_button),
                        ft.Container(content=exit_button),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
                width=300,
                height=320,
            ),
        )
        page.dialog = profile_dialog
        profile_dialog.open = True
        page.update()

    edit_button.on_click = edit_profile
    exit_button.on_click = exit_profile
    # Привязываем событие нажатия к открытию диалогового окна
    profile_button = ft.Container(
        content=account_button,
        width=190,
        height=40,
        padding=ft.padding.only(right=20),
        on_click=show_profile_dialog,
    )

    # Шапка приложения с кнопками
    header_container = ft.Container(
        content=ft.Row(
            [
                profile_button
            ],
            alignment=ft.MainAxisAlignment.END,
            expand=True,
        ),
    )

    screen_app_content = ft.Column(
        [
            header_container,
        ],
        expand=True
    )

    page.add(screen_app_content)
