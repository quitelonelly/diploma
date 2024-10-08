import threading
import flet as ft
import time
from database.core import get_user_id_by_login, insert_task, update_task

def main_screen(page, login, password):
    
    input_task = ft.TextField(
        label="Поиск",
        hint_text="Поиск задачи",
        text_size=14,
        width=290,
        color="#a0cafd",
        max_lines=1,
        prefix_icon=ft.icons.SEARCH,
    )
    
    input_task = ft.TextField(
        label="Поиск",
        hint_text="Поиск задачи",
        text_size=14,
        width=290,
        color="#a0cafd",
        border_color="white",
        max_lines=1,
        prefix_icon=ft.icons.SEARCH,
    )
    
    my_task_button = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(ft.icons.ACCOUNT_BOX),
                ft.Text("МОИ ЗАДАЧИ", size=14),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        on_click=lambda e: my_task_app(),
        width=150
    )

    all_task_button = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(ft.icons.FOLDER),
                ft.Text("ВСЕ ЗАДАЧИ", size=14),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        on_click=lambda e: all_task_app(),
        width=150
    )

    completed_button = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(ft.icons.TASK_OUTLINED),
                ft.Text("ВЫПОЛНЕНО", size=14),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        on_click=lambda e: done_app(),
        width=150
    )
    
     # Создаем кнопку навигации
    title_app = ft.Container(
        content=ft.Text("Pulse", size=18, weight="bold", color="#f7f7f7", font_family="Montserrat"),
        padding=ft.padding.only(left=20)
    )
    
    # Создаем кнопку "Личный кабинет"
    account_button = ft.Row(
        [
            ft.Icon(ft.icons.ACCOUNT_CIRCLE),
            ft.Text("Личный кабинет", weight=ft.FontWeight.BOLD, color="#a0cafd"),
            ft.Icon(ft.icons.ARROW_DROP_DOWN),
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
    
    # Функции замены контента в главном контейнере    
    def my_task_app():
        print("Мои задачи")
        main_container.content = panel_my_tasks
        page.update()
        
    def all_task_app():
        print("Все задачи")
        main_container.content = panel_all_tasks
        page.update()
        
    def done_app():
        print("Важное")
        main_container.content = panel_done
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
    
    all_task_list = ft.ListView(spacing=30, expand=True, padding=ft.padding.only(top=20))
    
    def open_task(e, task_container):
        content_container = task_container.content.controls[2]
        if not task_container.is_open:  # если контейнер не расширен
            for i in range(0, 300, 10):  # цикл для изменения высоты контейнера
                content_container.height = i
                page.update()
                time.sleep(0.007)  # задержка для создания анимации
            task_container.is_open = True
        else:  # если контейнер уже расширен
            for i in range(300, 0, -10):  # цикл для изменения высоты контейнера
                content_container.height = i
                page.update()
                time.sleep(0.007)  # задержка для создания анимации
            task_container.is_open = False
    
    def confirm_name_task(title_task, task_id, e):
        update_task(task_id, title_task.value)
        
        print(f"Имя " + title_task.value + " сохранено!")
        
    def add_task(e):
        print("Добавлена задача")
        
        title_task = ft.TextField(hint_text="Задача", text_size=22, color="#a0cafd", read_only=False, border_width=0, width=None, max_lines=2, expand=True)
        
        user_id = get_user_id_by_login(login)
        task_id = insert_task("Новая задача", user_id)
        
        open_task_button = ft.TextButton(
            content=ft.Row(
                [
                    ft.Text("Посмотреть все"),
                    ft.Icon(ft.icons.ARROW_DROP_DOWN)
                ],
                width=135
            ),
            on_click=lambda e: open_task(e, task_container),
            expand=True,
        )
        
        task_container = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            title_task,
                            ft.IconButton(ft.icons.CHECK, icon_color=ft.colors.GREEN, tooltip="Сохранить заголовок", on_click=lambda e, title_task=title_task, task_id=task_id: confirm_name_task(title_task, task_id, e))
                        ],
                    ),
                    open_task_button,
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Тут будет список задач", color=ft.colors.BLACK)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10,
                        ),
                        padding=ft.padding.all(10),
                        height=0,  # начальная высота контейнера
                    ),
                ],
            ),
            bgcolor="#f7f7f7",
            border_radius=10,
            padding=ft.padding.all(10)
        )
        task_container.is_open = False  # добавляем атрибут is_open
        all_task_list.controls.append(task_container)
        page.update()
        
    # Шапка приложения с кнопками
    header_container = ft.Container(
        content=ft.Row(
            [
                title_app,
                profile_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        ),
        border=ft.Border(bottom=ft.BorderSide(1))
    )
    
    # Контейнер с навигацией
    navigation_container = ft.Container(
        content=ft.Column(
            [
                input_task,
                my_task_button,
                all_task_button,
                completed_button
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
            expand=True,
        ),
        padding=ft.padding.only(left=10),
        width=320,
        border=ft.Border(right=ft.BorderSide(1))
    )
    
    # Контейнер с "Задачи"
    panel_my_tasks = ft.Container(
        content=ft.Column(  
            [   
                ft.Row(
                    [
                        ft.Text("Мои задачи", style="headlineMedium"),
                    ],
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            expand=True,
        ),
        padding=ft.padding.all(10),
    )
    
    # Контейнер с "Все задачи"
    panel_all_tasks = ft.Container(
        content=ft.Column(  
            [   
                ft.Row(
                    [
                        ft.Text("Все задачи", style="headlineMedium"),
                        ft.IconButton(ft.icons.ADD_TASK, icon_color=ft.colors.GREEN, tooltip="Добавить задачу", on_click=add_task)
                    ],
                    spacing=10,
                ),
                
                ft.Container(
                    content=all_task_list,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            expand=True,
        ),
        padding=ft.padding.all(10),
    )

    
    # Контейнер с "Важное"
    panel_done = ft.Container(
        content=ft.Column(  
            [   
                ft.Row(
                    [
                        ft.Text("Выполнено", style="headlineMedium"),
                    ],
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            expand=True,
        ),
        padding=ft.padding.all(10),
    )
    
    # Основной контейнер с функционалом приложения
    main_container = ft.Container(  
         content=panel_my_tasks,  
         expand=True,
         padding=ft.padding.all(20)
     )
    
    # Контент экрана
    screen_app_content = ft.Column(
        [
            header_container,
            ft.Row(
                [
                    navigation_container,
                    main_container
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
            )
        ],
        expand=True
    )

    page.add(screen_app_content)
