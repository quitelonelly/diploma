import flet as ft
import time

from threading import Timer

from database.core import (
    insert_task, update_task, get_tasks, get_users, insert_person, get_associated_users, remove_user_from_task, 
    get_user_id_by_login, get_responsible_users, delete_task, insert_subtask, update_subtask
    )

from frontend.layout import (
    create_input_task, create_my_task_btn, create_all_task_btn, create_completed_btn, create_account_btn,
    create_edit_btn, create_exit_btn, create_profile_dialog, create_task_container, create_header_container,
    create_nav_container, create_panel_my_task, create_panel_all_tasks, create_panel_done, create_screen_app,
    create_add_person_dialog, create_my_task_container, create_responsible_person_dialog, create_confirm_delete_task_dialog,
)

def main_screen(page, login, password):

    # Фукнция подтвержления изменения задачи   
    def confirm_name_task(title_task, task_id, e):
        update_task(task_id, title_task.value)
        
        print(f"Имя " + title_task.value + " сохранено!")
        
    # Функция открывает контейнер задачи    
    def open_task(task_container, e):
        content_container = task_container.content.controls[2]
        if not task_container.is_open:  # если контейнер не расширен
            for i in range(0, 380, 10):  # цикл для изменения высоты контейнера
                content_container.height = i
                page.update()
                time.sleep(0.007)  # задержка для создания анимации
            task_container.is_open = True
        else:  # если контейнер уже расширен
            for i in range(380, 0, -10):  # цикл для изменения высоты контейнера
                content_container.height = i
                page.update()
                time.sleep(0.007)  # задержка для создания анимации
            task_container.is_open = False
    
    # Списки с задачами       
    all_task_list = ft.ListView(spacing=30, expand=True, padding=ft.padding.only(top=20))
    
    my_task_list = ft.ListView(spacing=30, expand=True, padding=ft.padding.only(top=20))
    
    # Функция добавляет пользователя в задачу
    def add_people(task_id, e):
        show_add_person_dialog(task_id, e)
        
    # Функция показывает диалоговое окно с профилем
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
    
    # Функция показывает диалоговое окно добавления пользователя в задачу    
    def show_add_person_dialog(task_id, e):
        def close_dialog(dialog):
            dialog.open = False
            page.update()

        close_icon = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_color=ft.colors.WHITE,
            on_click=lambda _: close_dialog(add_person_dialog)
        )

        add_person_dialog = create_add_person_dialog(get_users, close_icon, page, insert_person, task_id, get_associated_users, remove_user_from_task)
        page.dialog = add_person_dialog
        add_person_dialog.open = True
        page.update()
    
    # Функция показывает диалоговое окно с исполнителями задачи    
    def show_responsible_users_dialog(task_id, e):
        def close_dialog(dialog):
            dialog.open = False
            page.update()
            
        close_icon = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_color=ft.colors.WHITE,
            on_click=lambda _: close_dialog(responsible_users_dialog)
        )

        responsible_users_dialog = create_responsible_person_dialog(get_responsible_users, task_id, get_users, close_icon)
        page.dialog = responsible_users_dialog
        responsible_users_dialog.open = True
        page.update()
        
    def show_confirm_delete_task_dialog(task_id, e, task_container, all_task_list, page):
        def close_dialog(dialog):
            dialog.open = False
            page.update()
            
        close_icon = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_color=ft.colors.WHITE,
            on_click=lambda _: close_dialog(confirm_delete_task_dialog)
        )

        confirm_delete_task_dialog = create_confirm_delete_task_dialog(delete_task, task_id, task_container, all_task_list, page, close_icon)
        page.dialog = confirm_delete_task_dialog
        confirm_delete_task_dialog.open = True
        page.update()
        
    # Функция добавляет задачу в список        
    def add_task(e):
        print("Добавлена задача")
        
        title_task = "Новая задача"
        task_id = insert_task(title_task)
        task_container = create_task_container(task_id, title_task, confirm_name_task, open_task, 
                                               add_people, all_task_list, page, show_confirm_delete_task_dialog, add_subtask)
        all_task_list.controls.append(task_container)
        page.update()    
     
    def add_subtask(task_id, in_all_task_list, e):
        print("Добавлена подзадача")
        
        # Создаем текстовое поле для ввода имени подзадачи
        subtask_input = ft.TextField(
            label="Введите название", 
            border_width=0, 
            autofocus=True,
            width=250,
            max_lines=5
        )

        # Создаем чекбокс для подзадачи
        subtask_checkbox = ft.Checkbox(
            value=False,
            on_change=lambda e: toggle_subtask(subtask_input.value, e.control.value)  # Обработчик изменения состояния
        )

        # Создаем строку, содержащую чекбокс и текстовое поле
        subtask_row = ft.Row(
            controls=[
                subtask_checkbox,
                subtask_input
            ],
            alignment=ft.MainAxisAlignment.START
        )
        
        # Вставляем подзадачу в базу данных с начальным значением "Новая подзадача"
        subtask_id = insert_subtask("Новая подзадача", task_id)

        # Переменная для хранения таймера
        update_timer = None

        # Обработчик для обновления подзадачи в базе данных при изменении текста
        def on_change_subtask_name(e):
            nonlocal update_timer
            # Отменяем предыдущий таймер, если он существует
            if update_timer is not None:
                update_timer.cancel()

            # Устанавливаем новый таймер на 1 секунду
            update_timer = Timer(5.0, lambda: update_subtask(subtask_id, subtask_input.value))
            update_timer.start()

        # Привязываем обработчик изменения текстового поля
        subtask_input.on_change = on_change_subtask_name

        # Добавляем строку с чекбоксом в список подзадач
        in_all_task_list.controls.append(subtask_row)
        in_all_task_list.update()  # Обновляем список подзадач
        page.update()  # Обновляем страницу

        # Очищаем текстовое поле после добавления
        subtask_input.value = ""

    # Обработчик для переключения состояния подзадачи
    def toggle_subtask(name, is_checked):
        if is_checked:
            print(f"Подзадача '{name}' выполнена!")
        else:
            print(f"Подзадача '{name}' не выполнена!")
    
    # Функция для интервального вызова функции    
    def repeater(interval, function):
        Timer(interval, repeater, [interval, function]).start()
        function()
    
    # Функция загружает все задачи
    def load_tasks():
        tasks = get_tasks()
        
        for task in tasks:
            if not any(container.task_id == task.id for container in all_task_list.controls):
                task_container = create_task_container(task.id, task.taskname, confirm_name_task, open_task, 
                                                       add_people, all_task_list, page, show_confirm_delete_task_dialog, add_subtask)
                all_task_list.controls.append(task_container)
        page.update()

    # Функция загружает мои задачи
    def load_my_tasks():
        my_task_list.controls.clear()
        user_id = get_user_id_by_login(login)
        tasks = get_tasks()
        
        for task in tasks:
            responsible_users = get_responsible_users(task.id)
            if user_id in responsible_users and not any(container.task_id == task.id for container in my_task_list.controls):
                task_container = create_my_task_container(task.id, task.taskname, confirm_name_task, open_task, show_responsible_users_dialog)
                my_task_list.controls.append(task_container)
        page.update()
    
    # Интервальный вызов функций обновления списков задач
    repeater(300, load_my_tasks)
    repeater(300, load_tasks)
            
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
        print("Выполнено")
        main_container.content = panel_done
        page.update()
        
    # Функции кнопок "Редактировать" и "Выйти"
    def edit_profile(e):
        print("Редактирование профиля")

    def exit_profile(e):
        print("Выход из профиля")
        
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
            title=ft.Text(login, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=24, overflow=ft.TextOverflow.ELLIPSIS, width=280),
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
    
    # Контейнер с "Мои задачи"
    panel_my_tasks = create_panel_my_task(my_task_list, load_my_tasks)
    
    # Контейнер с "Все задачи"
    panel_all_tasks = create_panel_all_tasks(add_task, all_task_list)

    
    # Контейнер с "Выполнено"
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
