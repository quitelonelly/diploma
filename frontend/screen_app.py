import flet as ft
import time
from database.core import insert_task, update_task, get_tasks
from frontend.layout import (
    create_input_task, create_my_task_btn, create_all_task_btn, create_completed_btn, create_account_btn,
    create_edit_btn, create_exit_btn, create_profile_dialog, create_task_container, create_header_container,
    create_nav_container, create_panel_my_task, create_panel_all_tasks, create_panel_done, create_screen_app
)

def main_screen(page, login, password):

    # Фукнция подтвержления изменения задачи   
    def confirm_name_task(title_task, task_id, e):
        update_task(task_id, title_task.value)
        
        print(f"Имя " + title_task.value + " сохранено!")
        
    # Функция открывает контейнер задачи    
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
            
    all_task_list = ft.ListView(spacing=30, expand=True, padding=ft.padding.only(top=20))
    
    def add_people(e):
        print("Добавлен исполнитель!")
    
    # Функция загружает задачи
    def load_tasks():
        tasks = get_tasks()
        
        for task in tasks:
            task_container = create_task_container(task.id, task.taskname, confirm_name_task, open_task, add_people)
            all_task_list.controls.append(task_container)
            page.update()
            
    load_tasks()
            
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
        
    # Функции кнопок "Редактировать" и "Выйти"
    def edit_profile(e):
        print("Редактирование профиля")

    def exit_profile(e):
        print("Выход из профиля")
    
    # Функция добавляет задачу в список        
    def add_task(e):
        print("Добавлена задача")
        
        title_task = "Новая задача"
        task_id = insert_task(title_task)
        task_container = create_task_container(task_id, title_task, confirm_name_task, open_task, add_people)
        all_task_list.controls.append(task_container)
        page.update()
    
    # Создание кнопок навигации и инпута поиска
    input_task = create_input_task()
    
    my_task_button = create_my_task_btn(my_task_app)

    all_task_button = create_all_task_btn(all_task_app)

    completed_button = create_completed_btn(done_app)
    
     # Создание заголовка
    title_app = ft.Container(
        content=ft.Text("Pulse", size=18, weight="bold", color="#f7f7f7", font_family="Montserrat"),
        padding=ft.padding.only(left=20)
    )
    
    # Создаем кнопку "Личный кабинет"
    account_button = create_account_btn()

    # Маскируем пароль звёздочками
    masked_password = "*" * len(password)

    # Подсказка в окне редактирования логина
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

    # Создаем кнопку "Редактировать"
    edit_button = create_edit_btn()

    # Создаем кнопку "Выйти" с другим стилем
    exit_button = create_exit_btn()
        
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

        profile_dialog = create_profile_dialog(close_icon, login_tile_container, password_tile_container, edit_button, exit_button)
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
    header_container = create_header_container(title_app, profile_button)
    
    # Контейнер с навигацией
    navigation_container = create_nav_container(input_task, my_task_button, all_task_button, completed_button)
    
    # Контейнер с "Задачи"
    panel_my_tasks = create_panel_my_task()
    
    # Контейнер с "Все задачи"
    panel_all_tasks = create_panel_all_tasks(add_task, all_task_list)

    
    # Контейнер с "Важное"
    panel_done = create_panel_done()
    
    # Основной контейнер с функционалом приложения
    main_container = ft.Container(  
         content=panel_my_tasks,  
         expand=True,
         padding=ft.padding.all(20)
     )
    
    # Контент экрана
    screen_app_content = create_screen_app(header_container, navigation_container, main_container)

    page.add(screen_app_content)
