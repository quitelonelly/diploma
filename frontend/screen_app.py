# Импортируем необходимые библиотеки
import asyncio
import flet as ft
import time
import os

from threading import Timer

from frontend.requests import (
    request_add_subtask, request_get_my_tasks, request_get_user_role, request_add_task, request_confirm_name_task, 
    request_get_tasks, request_get_subtasks, request_add_responsible, request_delete_responsible, request_get_users, request_update_comment, 
    request_update_subtask_status, request_delete_task, request_add_file, request_get_files_by_task_id, request_get_file,
    request_delete_file, request_get_responsible_by_task
    )

from database.core import (
    get_subtasks, insert_task, update_task, get_tasks, get_users, insert_person, get_associated_users, remove_user_from_task, 
    get_user_id_by_login, get_responsible_users, delete_task, insert_subtask, update_subtask, update_subtask_status,
    get_role_user, insert_file, get_files_by_task, delete_file, update_task_status, update_user
    )

from frontend.layout import (
    create_input_task, create_my_task_btn, create_all_task_btn, create_completed_btn, create_account_btn,
    create_edit_btn, create_exit_btn, create_profile_dialog, create_task_container, create_header_container,
    create_nav_container, create_panel_my_task, create_panel_all_tasks, create_panel_done, create_screen_app,
    create_add_person_dialog, create_my_task_container, create_responsible_person_dialog, create_confirm_delete_task_dialog,
    create_files_dialog, create_progress_bar, create_completed_task_container, create_update_profile_dialog
)

async def main_screen(page, login, password, token):
    
    page.window.resizable = False

    # Функция для получения роли пользователя
    async def get_user_role():
        response = await request_get_user_role(login)
        
        if response.status_code == 200:
            role = response.text.strip().replace('"', '')  # Удаляем пробелы и кавычки
            print(f"Полученная роль: {role}")  # Логируем полученную роль
            if role == "ADMIN":
                print("Вы вошли как администратор!")
                return True
            else:
                print("Вы вошли как пользователь!")
                return False
        else:
            print(f"Ошибка при получении роли: {response.status_code}, {response.text}")
            return False  # Если произошла ошибка, возвращаем False
    
    admin_role = await get_user_role()

    # Фукнция подтвержления изменения задачи   
    async def confirm_name_task(title_task, task_id, e):
        try:
            response = await request_confirm_name_task(task_id, title_task)
            if response.status_code == 200:
                print("Название задачи успешно изменено!")
            else:
                print(f"Ошибка при изменении названия задачи: {response.status_code}, {response.text}")
        except ValueError:
            print("Ошибка")

    # Функция открывает контейнер задачи    
    def open_task(task_container, e):
        content_container = task_container.content.controls[2]
        if not task_container.is_open:  # если контейнер не расширен
            for i in range(0, 390, 10):  # цикл для изменения высоты контейнера
                content_container.height = i
                page.update()
                time.sleep(0.007)  # задержка для создания анимации
            task_container.is_open = True
        else:  # если контейнер уже расширен
            for i in range(390, 0, -10):  # цикл для изменения высоты контейнера
                content_container.height = i
                page.update()
                time.sleep(0.007)  # задержка для создания анимации
            task_container.is_open = False
    
    # Списки с задачами       
    all_task_list = ft.ListView(spacing=30, expand=True, padding=ft.padding.only(top=20))
    
    my_task_list = ft.ListView(spacing=30, expand=True, padding=ft.padding.only(top=20))
    
    completed_task_list = ft.ListView(spacing=30, expand=True, padding=ft.padding.only(top=20))

    # Функция добавляет пользователя в задачу
    def add_people(task_id, e):
        asyncio.run(show_add_person_dialog(task_id, e))

    # Функция показывает диалоговое окно с загруженными файлами
    def get_files(task_id, e):
        show_files_dialog(task_id, e)
        
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
    async def show_add_person_dialog(task_id, e):
        def close_dialog(dialog):
            dialog.open = False
            page.update()

        close_icon = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_color=ft.colors.WHITE,
            on_click=lambda _: close_dialog(add_person_dialog)
        )

        # Ожидаем результат от request_get_users
        users = await request_get_users()  # Получаем пользователей через API

        # Получаем связанных пользователей через API
        associated_users_response = await request_get_responsible_by_task(task_id)
        associated_users = []
        if associated_users_response.status_code == 200:
            data = associated_users_response.json()  # Получаем данные в формате JSON
            associated_users = data.get("responsibles", [])  # Извлекаем список исполнителей
        else:
            print(f"Ошибка при получении связанных пользователей: {associated_users_response.status_code}, {associated_users_response.text}")

        add_person_dialog = create_add_person_dialog(
            users,  # Передаем пользователей в диалог
            close_icon, 
            page, 
            request_add_responsible, 
            task_id, 
            associated_users,  # Передаем связанных пользователей
            request_delete_responsible
        )
        
        page.dialog = add_person_dialog
        add_person_dialog.open = True
        page.update()

    # Функция показывает диалоговое окно c файлами
    def show_files_dialog(task_id, e):
        def close_dialog(dialog):
            dialog.open = False
            page.update()

        close_icon = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_color=ft.colors.WHITE,
            on_click=lambda _: close_dialog(files_dialog)
        )

        files_dialog = create_files_dialog(task_id, download_file, request_get_files_by_task_id, close_icon, request_delete_file, page)
        page.dialog = files_dialog
        files_dialog.open = True
        page.update()
    
    # Функция показывает диалоговое окно с исполнителями задачи    
    async def show_responsible_users_dialog(task_id, e):
        def close_dialog(dialog):
            dialog.open = False
            page.update()

        close_icon = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_color=ft.colors.WHITE,
            on_click=lambda _: close_dialog(responsible_users_dialog)
        )

        # Ожидаем результат от request_get_responsible_by_task
        response = await request_get_responsible_by_task(task_id)
        
        if response.status_code == 200:
            data = response.json()  # Получаем данные в формате JSON
            responsible_users = data.get("responsibles", [])  # Извлекаем список исполнителей
        else:
            print(f"Ошибка при получении исполнителей: {response.status_code}, {response.text}")
            responsible_users = []  # Если ошибка, устанавливаем пустой список

        responsible_users_dialog = create_responsible_person_dialog(responsible_users, close_icon)
        page.dialog = responsible_users_dialog
        responsible_users_dialog.open = True
        page.update()

    # Функция показывает диалоговое окно с удалением задачи    
    def show_confirm_delete_task_dialog(task_id, e, task_container, all_task_list, page):
        def close_dialog(dialog):
            dialog.open = False
            page.update()
            
        close_icon = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_color=ft.colors.WHITE,
            on_click=lambda _: close_dialog(confirm_delete_task_dialog)
        )

        confirm_delete_task_dialog = create_confirm_delete_task_dialog(request_delete_task, task_id, task_container, all_task_list, page, close_icon)
        page.dialog = confirm_delete_task_dialog
        confirm_delete_task_dialog.open = True
        page.update()

    def show_update_profile_dialog(update_user, login):

        def close_dialog(dialog):
            dialog.open = False
            page.update()

        close_icon = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_color=ft.colors.WHITE,
            on_click=lambda _: close_dialog(update_profile_dialog)
        )

        # Создаем текстовые поля для нового логина и пароля
        new_username_input = ft.TextField(label="Новый логин", width=320)
        new_password_input = ft.TextField(label="Новый пароль", width=320, password=True)

        # Кнопка для сохранения изменений
        save_button = ft.CupertinoFilledButton(
            text="Сохранить",
            width=320,
            on_click=lambda e: update_user(login, new_username_input.value, new_password_input.value)
        )

        update_profile_dialog = create_update_profile_dialog(
            close_icon, new_username_input, new_password_input, save_button
        )

        page.dialog = update_profile_dialog
        update_profile_dialog.open = True
        page.update()

    async def download_file(file_id: int, file_name: str):
        # Запрашиваем файл по ID
        file_data = await request_get_file(file_id)
        
        if file_data is not None:
            # Определяем путь к папке "Загрузки"
            save_path = os.path.join(os.path.expanduser("~"), "Загрузки", file_name)

            # Записываем данные файла в файл
            with open(save_path, 'wb') as f:
                f.write(file_data)

            print(f"Файл '{file_name}' успешно загружен в '{save_path}'")
        else:
            print(f"Не удалось загрузить файл с ID {file_id}.")

    def add_file(file_container, task_id, e):
        print("Открываем файл...")

        # Инициализация FilePicker
        file_picker = ft.FilePicker(on_result=lambda e: asyncio.run(pick_files_result(e, file_container, task_id)))

        # Добавляем FilePicker в overlay
        page.overlay.append(file_picker)
        # Обновляем страницу, чтобы убедиться, что FilePicker добавлен
        page.update()

        # Теперь, когда FilePicker добавлен, вызываем pick_files
        file_picker.pick_files(allow_multiple=False)

    async def pick_files_result(e: ft.FilePickerResultEvent, file_container, task_id):
        if e.files:
            file_path = e.files[0].path  # Получаем полный путь к файлу
            file_name = os.path.basename(file_path)  # Извлекаем только имя файла

            # Теперь вызываем запрос на добавление файла
            with open(file_path, 'rb') as f:
                file_data = f.read()  # Читаем данные файла

            # Теперь вызываем запрос на добавление файла
            response = await request_add_file(task_id, file_name, file_data)  # Передаем имя файла и данные

            if response.status_code == 201:
                print("Файл успешно загружен!")
            else:
                print(f"Ошибка при загрузке файла: {response.status_code}, {response.text}")

            # Обновляем интерфейс, чтобы отобразить имя файла
            file_container.update()  # Обновление контейнера файла
        else:
            print("Файл не выбран")

        file_container.update()
        
    # Функция добавляет задачу в список        
    async def add_task(e):
        print("Добавлена задача")
        
        title_task = "Новая задача"  # Здесь вы можете получить название задачи от пользователя, например, из текстового поля
        response = await request_add_task(title_task)  # Отправляем запрос на добавление задачи

        if response.status_code == 200:
            task_id = response.json().get("task_id")  # Получаем ID новой задачи из ответа
            print(f"Задача успешно добавлена с ID: {task_id}")
            
            # Например, добавьте задачу в список задач
            progress_bar = create_progress_bar()  # Создаем прогресс-бар для новой задачи
            task_container = create_task_container(task_id, title_task, '', confirm_name_task, open_task, 
                                                add_people, all_task_list, page, show_confirm_delete_task_dialog, add_subtask,
                                                admin_role, show_responsible_users_dialog, add_file, get_files, progress_bar,
                                                update_comment)
            all_task_list.controls.append(task_container)
            page.update()    
        else:
            print(f"Ошибка при добавлении задачи: {response.status_code}, {response.text}")

    # Добавим функцию для обновления комментария
    async def update_comment(task_id, comment_text):
        try:
            response = await request_update_comment(task_id, comment_text)
            if response.status_code == 200:
                print("Комментарий успешно обновлен!")
            else:
                print(f"Ошибка при обновлении комментария: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Ошибка при обновлении комментария: {e}")

    # Функция для создания контейнера подзадачи
    def create_subtask_container(subtask_id, task_id, subtask_name, process_list, test_list, completed_list, progress_bar):

        # Создаем текстовое поле для имени подзадачи
        subtask_input = ft.TextField(
            label="Название подзадачи",
            value=subtask_name,
            border_width=0,
            autofocus=True,
            width=240,
            max_lines=5
        )

        # Создаем чекбокс для подзадачи
        subtask_checkbox = ft.Checkbox(
            value=False,
            on_change=lambda e: toggle_subtask(
                subtask_input.value, e.control.value, process_list, test_list,
                completed_list, subtask_row, subtask_id, task_id, e
            )
        )

        # Создаем строку, содержащую чекбокс и текстовое поле
        subtask_row = ft.Row(
            controls=[
                subtask_checkbox,
                subtask_input
            ],
            alignment=ft.MainAxisAlignment.START
        )

        # Обработчик для обновления подзадачи в базе данных при изменении текста
        def on_change_subtask_name(e):
            asyncio.run(request_update_subtask_status(subtask_id, subtask_input.value))

        # Привязываем обработчик изменения текстового поля
        subtask_input.on_change = on_change_subtask_name
        return subtask_row
    
    # Функция добавляет подзадачу в список 
    async def add_subtask(task_id, name, process_list, test_list, completed_list, progress_bar, e):
        print("Добавлена подзадача")

        # Отправляем запрос на добавление подзадачи через API
        response = await request_add_subtask(task_id, name)

        if response.status_code == 200:
            subtask_id = response.json().get("subtask_id")  # Получаем ID новой подзадачи из ответа
            print(f"Подзадача успешно добавлена с ID: {subtask_id}")

            # Создаем текстовое поле для ввода имени подзадачи
            subtask_input = ft.TextField(
                label="Название подзадачи",
                value=name,
                border_width=0, 
                autofocus=True,
                width=240,
                max_lines=5
            )

            # Создаем чекбокс для подзадачи
            subtask_checkbox = ft.Checkbox(
                value=False,
                on_change=lambda e: toggle_subtask(
                    subtask_input.value, e.control.value, process_list, test_list, 
                    completed_list, subtask_row, subtask_id, task_id, e
                )
            )

            # Создаем строку, содержащую чекбокс и текстовое поле
            subtask_row = ft.Row(
                controls=[
                    subtask_checkbox,
                    subtask_input
                ],
                alignment=ft.MainAxisAlignment.START
            )

            # Обработчик для обновления подзадачи в базе данных при изменении текста
            def on_change_subtask_name(e):
                update_subtask(subtask_id, subtask_input.value)

            # Привязываем обработчик изменения текстового поля
            subtask_input.on_change = on_change_subtask_name

            # Добавляем строку с чекбоксом в список подзадач
            process_list.controls.append(subtask_row)

            page.update()  # Обновляем страницу
        else:
            print(f"Ошибка при добавлении подзадачи: {response.status_code}, {response.text}")


    # Функция для интервального вызова функции    
    def repeater(interval, function):
        Timer(interval, repeater, [interval, function]).start()
        asyncio.create_task(function())  # Запускаем корутину без asyncio.run()

    # Функция для выгрузки задач из БД
    async def load_my_tasks(filtered_task=None):
        my_task_list.controls.clear()  # Очищаем текущий список задач

        user_id = get_user_id_by_login(login)  # Получаем ID пользователя

        # Получаем задачи из API
        response = await request_get_my_tasks(user_id)  # Используем запрос к API

        if response.status_code == 200:
            tasks = response.json()  # Предполагаем, что API возвращает список задач в формате JSON
            print(f"Полученные задачи: {tasks}")  # Отладочное сообщение

            # Фильтруем задачи, если передан параметр filtered_task
            if filtered_task:
                tasks = [task for task in tasks if task['taskname'] in filtered_task]

            for task in tasks:
                responsible_users = get_responsible_users(task['id'])
                if user_id in responsible_users and not any(container.task_id == task['id'] for container in my_task_list.controls):

                    if task['status'] == "Выполнено":
                        continue

                    progress_bar = create_progress_bar()

                    task_container = create_my_task_container(
                        task['id'], 
                        task['taskname'],  
                        task['comment'],
                        open_task, 
                        show_responsible_users_dialog, 
                        add_file, 
                        get_files,
                        progress_bar,
                        update_comment
                    )

                    # Получаем подзадачи для текущей задачи через API
                    subtask_response = await request_get_subtasks(task['id'])
                    if subtask_response.status_code == 200:
                        task_subtasks = subtask_response.json()  # Получаем подзадачи
                    else:
                        print(f"Ошибка при получении подзадач: {subtask_response.status_code}, {subtask_response.text}")
                        task_subtasks = []  # Если ошибка, устанавливаем пустой список подзадач

                    process_list = task_container.in_all_task_list_process
                    test_list = task_container.in_all_task_list_test
                    completed_list = task_container.in_all_task_list_completed

                    # Обновляем прогресс-бар
                    total_subtasks = len(task_subtasks)
                    completed_count = sum(1 for subtask in task_subtasks if subtask['status'] == "Готово")

                    # Логирование для отладки
                    print(f"Задача: {task['taskname']}, Общее количество подзадач: {total_subtasks}, Выполненные: {completed_count}")

                    # Обновление значения прогресс-бара
                    if total_subtasks > 0:
                        progress_bar.value = completed_count / total_subtasks 
                    else:
                        progress_bar.value = 0

                    # Добавляем подзадачи в соответствующие списки
                    for subtask in task_subtasks:
                        if subtask['status'] == "В процессе":
                            subtask_row = create_subtask_container(subtask['id'], task['id'], subtask['subtaskname'], process_list, test_list, completed_list, progress_bar)
                            process_list.controls.append(subtask_row)
                        elif subtask['status'] == "На проверке":
                            if admin_role:
                                subtask_row = create_subtask_container(subtask['id'], task['id'], subtask['subtaskname'], process_list, test_list, completed_list, progress_bar)
                                test_list.controls.append(subtask_row)
                            else:
                                subtask_text_row = ft.Row(
                                    controls=[
                                        ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.YELLOW),
                                        ft.Text(subtask['subtaskname'], size=16, width=240, color=ft.colors.WHITE)
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                )
                                test_list.controls.append(subtask_text_row)
                        elif subtask['status'] == "Готово":
                            subtask_compl_row = ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.GREEN),
                                    ft.Text (subtask['subtaskname'], size=16, width=240, color=ft.colors.WHITE)
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            )
                            completed_list.controls.append(subtask_compl_row)

                    my_task_list.controls.append(task_container)

        else:
            print(f"Ошибка при получении задач: {response.status_code}, {response.text}")

        page.update()  # Обновляем страницу после загрузки задач

    async def load_tasks(filtered_task=None):
        all_task_list.controls.clear()

        # Получаем задачи из API
        response = await request_get_tasks()
        
        if response.status_code == 200:
            tasks = response.json()  # Предполагаем, что API возвращает список задач в формате JSON
        else:
            print(f"Ошибка при получении задач: {response.status_code}, {response.text}")
            return  # Выход из функции, если запрос не удался

        # Если есть фильтрация, используем отфильтрованные задачи
        if filtered_task:
            tasks = [task for task in tasks if task['taskname'] in filtered_task]

        for task in tasks:
            if not any(container.task_id == task['id'] for container in all_task_list.controls):
                if task['status'] == "Выполнено":
                    continue

                progress_bar = create_progress_bar()    
                
                task_container = create_task_container(
                    task['id'], task['taskname'], task['comment'], confirm_name_task, open_task,
                    add_people, all_task_list, page, show_confirm_delete_task_dialog,
                    add_subtask, admin_role, show_responsible_users_dialog,
                    add_file, get_files, progress_bar, update_comment
                )

                # Получаем подзадачи для текущей задачи через API
                subtask_response = await request_get_subtasks(task['id'])
                if subtask_response.status_code == 200:
                    task_subtasks = subtask_response.json()  # Получаем подзадачи
                else:
                    print(f"Ошибка при получении подзадач: {subtask_response.status_code}, {subtask_response.text}")
                    task_subtasks = []  # Если ошибка, устанавливаем пустой список подзадач

                process_list = task_container.in_all_task_list_process
                test_list = task_container.in_all_task_list_test
                completed_list = task_container.in_all_task_list_completed

                # Обновляем прогресс-бар
                total_subtasks = len(task_subtasks)
                completed_count = sum(1 for subtask in task_subtasks if subtask['status'] == "Готово")

                # Логирование для отладки
                print(f"Задача: {task['taskname']}, Общее количество подзадач: {total_subtasks}, Выполненные: {completed_count}")

                # Обновление значения прогресс-бара
                if total_subtasks > 0:
                    progress_bar.value = completed_count / total_subtasks 
                else:
                    progress_bar.value = 0

                # Добавляем подзадачи в соответствующие списки
                for subtask in task_subtasks:
                    if subtask['status'] == "В процессе":
                        subtask_row = create_subtask_container(subtask['id'], task['id'], subtask['subtaskname'], process_list, test_list, completed_list, progress_bar)
                        process_list.controls.append(subtask_row)
                    elif subtask['status'] == "На проверке":
                        if admin_role:
                            subtask_row = create_subtask_container(subtask['id'], task['id'], subtask['subtaskname'], process_list, test_list, completed_list, progress_bar)
                            test_list.controls.append(subtask_row)
                        else:
                            subtask_text_row = ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.YELLOW),
                                    ft.Text(subtask['subtaskname'], size=16, width=240, color=ft.colors.WHITE)
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            )
                            test_list.controls.append(subtask_text_row)
                    elif subtask['status'] == "Готово":
                        subtask_compl_row = ft.Row(
                            controls=[
                                ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.GREEN),
                                ft.Text(subtask['subtaskname'], size=16, width=240, color=ft.colors.WHITE)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        )
                        completed_list.controls.append(subtask_compl_row)

                all_task_list.controls.append(task_container)

        page.update()  # Обновляем страницу после загрузки задач

    async def load_comp_tasks(filtered_task=None):
        completed_task_list.controls.clear()  # Очищаем текущий список выполненных задач

        # Получаем задачи из API
        response = await request_get_tasks()  # Используем запрос к API

        if response.status_code == 200:
            tasks = response.json()  # Предполагаем, что API возвращает список задач в формате JSON
            print(f"Полученные задачи: {tasks}")  # Отладочное сообщение

            # Фильтруем выполненные задачи
            completed_tasks = [task for task in tasks if task['status'] == "Выполнено"]

            for task in completed_tasks:
                completed_list = ft.ListView(spacing=10, expand=True, padding=ft.padding.only(top=10, left=10))

                # Получаем подзадачи для текущей задачи через API
                subtask_response = await request_get_subtasks(task['id'])
                if subtask_response.status_code == 200:
                    task_subtasks = subtask_response.json()  # Получаем подзадачи
                else:
                    print(f"Ошибка при получении подзадач: {subtask_response.status_code}, {subtask_response.text}")
                    task_subtasks = []  # Если ошибка, устанавливаем пустой список подзадач

                # Добавляем подзадачи в список выполненных
                for subtask in task_subtasks:
                    if subtask['status'] == "Готово":
                        subtask_row = ft.Row(
                            controls=[
                                ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.GREEN),
                                ft.Text(subtask['subtaskname'], size=16, width=240, color=ft.colors.WHITE)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        )
                        completed_list.controls.append(subtask_row)

                # Создаем контейнер для выполненной задачи
                completed_task_container = create_completed_task_container(
                    task['id'],
                    task['taskname'],
                    open_task,
                    completed_list,
                    page,
                    show_responsible_users_dialog,
                    get_files,
                    completed_task_list,
                    show_confirm_delete_task_dialog
                )

                # Добавляем выполненную задачу в список "Выполнено"
                completed_task_list.controls.append(completed_task_container)

        else:
            print(f"Ошибка при получении задач: {response.status_code}, {response.text}")

        page.update()  # Обновляем страницу после загрузки задач

    # Функция обрабатывает отметку чекбоксов
    def toggle_subtask(name, is_checked, process_list, test_list, completed_list, subtask_row, subtask_id, task_id, e):
        print("Текущий список 'В процессе':", [row.controls[1].value for row in process_list.controls if isinstance(row, ft.Row)])
        print("Текущий список 'На проверке':", [row.controls[1].value for row in test_list.controls if isinstance(row, ft.Row)])
        print("Текущий список 'Готово':", [row.controls[1].value for row in completed_list.controls if isinstance(row, ft.Row)])

        # Проверяем, находится ли подзадача в списке "В процессе"
        if subtask_row in process_list.controls:
            if is_checked:
                print(f"Подзадача '{name}' выполнена!")
                # Удаляем подзадачу из списка "В процессе"
                process_list.controls.remove(subtask_row)

                if admin_role:
                    subtask_input = ft.TextField(
                        label="Название подзадачи",
                        value=name,
                        border_width=0, 
                        autofocus=True,
                        width=240,
                        max_lines=5
                    )

                    subtask_checkbox = ft.Checkbox(
                        value=False,
                        on_change=lambda e: toggle_subtask(
                            subtask_input.value, e.control.value, process_list, test_list, 
                            completed_list, subtask_row, subtask_id, task_id, e
                        )
                    )

                    # Создаем строку, содержащую чекбокс и текстовое поле
                    subtask_row = ft.Row(
                        controls=[
                            subtask_checkbox,
                            subtask_input
                        ],
                        alignment=ft.MainAxisAlignment.START
                    )

                    test_list.controls.append(subtask_row)
                    asyncio.run(request_update_subtask_status(subtask_id, "На проверке"))

                else:
                    subtask_text_row = ft.Row(
                        controls=[
                            ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.YELLOW),
                            ft.Text(name, size=16, width=240, color=ft.colors.WHITE)
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    )
                    test_list.controls.append(subtask_text_row)
                    asyncio.run(request_update_subtask_status(subtask_id, "На проверке"))
                    print("Подзадача добавлена в список 'На проверке'.")

        # Проверяем, находится ли подзадача в списке "На проверке"
        elif subtask_row in test_list.controls:
            if is_checked:

                print(f"Подзадача '{name}' выполнена!")
                # Удаляем подзадачу из списка "На проверке"
                test_list.controls.remove(subtask_row)

                subtask_text_completed_row = ft.Row(
                    controls=[
                        ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.GREEN),
                        ft.Text(name, size=16, width=240, color=ft.colors.WHITE)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
                # Добавляем подзадачу в список "Готово"
                completed_list.controls.append(subtask_text_completed_row)
                asyncio.run(request_update_subtask_status(subtask_id, "Готово"))
                print("Подзадача добавлена в список 'Готово'.")

        else:
            print(f"Подзадача '{name}' не выполнена!")

            # Устанавливаем значение чекбокса в False, чтобы подзадача была неотмеченной
            subtask_row.controls[0].value = False  # Устанавливаем чекбокс в неотмеченное состояние

        # Обновляем списки
        process_list.update()
        test_list.update()
        completed_list.update()

        # Обновляем прогресс-бар
        update_progress_bar(task_id, process_list, test_list, completed_list, all_task_list, my_task_list)

        page.update()  # Обновляем страницу после изменений

    # Функция обновляет прогресс бар
    def update_progress_bar(task_id, process_list, test_list, completed_list, all_task_list, my_task_list):
        total_subtasks = len(process_list.controls) + len(test_list.controls) + len(completed_list.controls)
        completed_count = len(completed_list.controls)

        # Обновление значения прогресс-бара
        if total_subtasks > 0:
            progress_value = completed_count / total_subtasks
        else:
            progress_value = 0

        # Обновляем прогресс-бар для текущей задачи в all_task_list
        for task_container in all_task_list.controls:
            if task_container.task_id == task_id:  # Найти соответствующий контейнер задачи
                task_container.progress_bar.value = progress_value  # Обновляем значение прогресс-бара
                break

        # Обновляем прогресс-бар для текущей задачи в my_task_list
        for task_container in my_task_list.controls:
            if task_container.task_id == task_id:  # Найти соответствующий контейнер задачи
                task_container.progress_bar.value = progress_value  # Обновляем значение прогресс-бара
                break

        # Проверяем, заполнен ли прогресс бар
        if progress_value == 1.0:  # Можно использовать '==' для точной проверки
            print("Задача выполнена!")
            update_task_status(task_id, "Выполнено")  # Обновляем статус задачи в базе данных
            
            # Создание контейнера для выполненной задачи
            completed_task_container = create_completed_task_container(
                task_id, 
                task_container.title_task.value, 
                open_task, 
                completed_list,
                page, 
                show_responsible_users_dialog, 
                get_files,
                completed_task_list,
                show_confirm_delete_task_dialog
            )
            print("Контейнер для выполненной задачи создан:", completed_task_container)

            # Удаляем контейнер задачи из списка активных задач
            task_to_remove = None
            for task_container in all_task_list.controls:
                if task_container.task_id == task_id:
                    task_to_remove = task_container
                    break

            if task_to_remove:
                all_task_list.controls.remove(task_to_remove)  # Удаляем контейнер задачи из "Все задачи"
            else:
                print(f"Контейнер с ID {task_id} не найден в списке активных задач.")

            # Удаляем контейнер задачи из списка "Мои задачи"
            for task_container in my_task_list.controls:
                if task_container.task_id == task_id:
                    my_task_list.controls.remove(task_container)  # Удаляем контейнер задачи из "Мои задачи"
                    break

            # Добавляем выполненную задачу в список "Выполнено"
            completed_task_list.controls.append(completed_task_container)
            print("Задача перемещена в список 'Выполнено'.")

            # Обновляем интерфейс после изменений
            page.update()  # Обновляем страницу после изменений
    
    # Интервальный вызов функций обновления списков задач
    repeater(300, load_my_tasks)
    repeater(300, load_tasks)
    repeater(200, load_comp_tasks)
            
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
        show_update_profile_dialog(update_user, login)

    def exit_profile(e):
        print("Выход из профиля")

    def search_task(search_query):
        # Получаем все задачи
        all_tasks = get_tasks()
        
        # Фильтруем задачи по запросу
        filtered_tasks = [task for task in all_tasks if search_query.lower() in task.taskname.lower()]

        # Обновляем main_container в зависимости от текущей выбранной панели
        if main_container.content == panel_my_tasks:
            my_task_list.controls.clear()
            asyncio.run(load_my_tasks(filtered_tasks)) # Передайте отфильтрованные задачи в функцию загрузки моих задач
        elif main_container.content == panel_all_tasks:
            all_task_list.controls.clear()
            asyncio.run(load_tasks(filtered_tasks))  # Передайте отфильтрованные задачи в функцию загрузки всех задач
        elif main_container.content == panel_done:
            completed_task_list.controls.clear()
            asyncio.run(load_comp_tasks(filtered_tasks)) # Передайте отфильтрованные задачи в функцию загрузки выполненных задач

        
    # Создание кнопок навигации и инпута поиска
    input_task = create_input_task(search_task)
    
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
    panel_all_tasks = create_panel_all_tasks(add_task, all_task_list, admin_role)

    # Контейнер с "Выполнено"
    panel_done = create_panel_done(completed_task_list, load_comp_tasks)
    
    # Основной контейнер с функционалом приложения
    main_container = ft.Container(  
         content=panel_my_tasks,  
         expand=True,
         padding=ft.padding.all(20)
     )
    
    # Контент экрана
    screen_app_content = create_screen_app(header_container, navigation_container, main_container)

    page.add(screen_app_content)
