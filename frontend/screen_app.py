# Импортируем необходимые библиотеки
import flet as ft
import time
import os

from threading import Timer

from database.core import (
    get_subtasks, insert_task, update_task, get_tasks, get_users, insert_person, get_associated_users, remove_user_from_task, 
    get_user_id_by_login, get_responsible_users, delete_task, insert_subtask, update_subtask, update_subtask_status,
    get_role_user, insert_file, get_files_by_task, delete_file, update_task_status
    )

from frontend.layout import (
    create_input_task, create_my_task_btn, create_all_task_btn, create_completed_btn, create_account_btn,
    create_edit_btn, create_exit_btn, create_profile_dialog, create_task_container, create_header_container,
    create_nav_container, create_panel_my_task, create_panel_all_tasks, create_panel_done, create_screen_app,
    create_add_person_dialog, create_my_task_container, create_responsible_person_dialog, create_confirm_delete_task_dialog,
    create_files_dialog, create_progress_bar, create_completed_task_container
)

def main_screen(page, login, password):
    
    page.window.resizable = False
    admin_role = get_role_user(login)
    
    if admin_role:
        print("Вы вошли как администратор!")
    else:
        print("Вы вошли как пользователь!")

    # Фукнция подтвержления изменения задачи   
    def confirm_name_task(title_task, task_id, e):
        update_task(task_id, title_task.value)
        
        print(f"Имя " + title_task.value + " сохранено!")
        
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
        show_add_person_dialog(task_id, e)

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

        files_dialog = create_files_dialog(task_id, download_file, get_files_by_task, close_icon, delete_file, page)
        page.dialog = files_dialog
        files_dialog.open = True
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

        confirm_delete_task_dialog = create_confirm_delete_task_dialog(delete_task, task_id, task_container, all_task_list, page, close_icon)
        page.dialog = confirm_delete_task_dialog
        confirm_delete_task_dialog.open = True
        page.update()

    import platform

    def download_file(file_data, file_name):

        # Определяем путь к папке "Загрузки"
        if platform.system() == "Windows":
            # Для Windows
            save_path = os.path.join(os.path.expanduser("~"), "Загрузки", file_name)
        elif platform.system() == "Darwin":
            # Для macOS
            save_path = os.path.join(os.path.expanduser("~"), "Загрузки", file_name)
        else:
            # Для Linux и других Unix-подобных систем
            save_path = os.path.join(os.path.expanduser("~"), "Загрузки", file_name)
        # Записываем данные файла в файл
        with open(save_path, 'wb') as f:
            f.write(file_data)

        print(f"Файл '{file_name}' успешно загружен в '{save_path}'")

    def add_file(file_container, task_id, e):
        print("Открываем файл...")

        # Инициализация FilePicker
        file_picker = ft.FilePicker(on_result=lambda e: pick_files_result(e, file_container, task_id))

        # Добавляем FilePicker в overlay
        page.overlay.append(file_picker)
        # Обновляем страницу, чтобы убедиться, что FilePicker добавлен
        page.update()

        # Теперь, когда FilePicker добавлен, вызываем pick_files
        file_picker.pick_files(allow_multiple=False)

    def pick_files_result(e: ft.FilePickerResultEvent, file_container, task_id):
        if e.files:
            file_path = e.files[0].path  # Получаем полный путь к файлу
            file_name = os.path.basename(file_path)  # Извлекаем только имя файла

            # Читаем файл в бинарном формате
            with open(file_path, 'rb') as file:
                file_data = file.read()  # Читаем файл в бинарном формате
                insert_file(task_id, file_name, file_data)  # Сохраняем файл в базе данных

            # Обновляем интерфейс, чтобы отобразить имя файла
            file_container.update()  # Обновление контейнера файла
        else:
            print("Файл не выбран")

        file_container.update()
        
    # Функция добавляет задачу в список        
    def add_task(e):
        print("Добавлена задача")
        
        title_task = "Новая задача"
        task_id = insert_task(title_task)

        progress_bar = create_progress_bar()

        task_container = create_task_container(task_id, title_task, confirm_name_task, open_task, 
                                               add_people, all_task_list, page, show_confirm_delete_task_dialog, add_subtask,
                                               admin_role, show_responsible_users_dialog, add_file, get_files, progress_bar)
        all_task_list.controls.append(task_container)
        page.update()    

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
            update_subtask(subtask_id, subtask_input.value)

        # Привязываем обработчик изменения текстового поля
        subtask_input.on_change = on_change_subtask_name
        return subtask_row
    
    # Функция добавляет подзадачу в список 
    def add_subtask(task_id, name, process_list, test_list, completed_list, progress_bar, e):

        print("Добавлена подзадача")

        # Вставляем подзадачу в базу данных с начальным значением "Новая подзадача"
        subtask_id = insert_subtask("Новая подзадача", task_id)

        # Создаем текстовое поле для ввода имени подзадачи
        subtask_input = ft.TextField(
            label="Название подзадачи",
            value=name,
            border_width=0, 
            autofocus=True,
            width=240,
            max_lines=5
        )


# name, is_checked, process_list, test_list, completed_list, subtask_row, subtask_id, task_id, e
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


    # Функция для интервального вызова функции    
    def repeater(interval, function):
        Timer(interval, repeater, [interval, function]).start()
        function()

    def load_my_tasks():
        my_task_list.controls.clear()

        user_id = get_user_id_by_login(login)

        tasks = get_tasks()
        subtasks = get_subtasks()

        for task in tasks:
            responsible_users = get_responsible_users(task.id)
            if user_id in responsible_users and not any(container.task_id == task.id for container in my_task_list.controls):

                if task.status == "Выполнено":
                    continue

                progress_bar = create_progress_bar()

                task_container = create_my_task_container(
                    task.id, 
                    task.taskname,  
                    open_task, 
                    show_responsible_users_dialog, 
                    add_file, 
                    get_files,
                    progress_bar
                )
                    
                # Находим подзадачи для текущей задачи
                task_subtasks = [subtask for subtask in subtasks if subtask.id_task == task.id]

                process_list = task_container.in_all_task_list_process
                test_list = task_container.in_all_task_list_test
                completed_list = task_container.in_all_task_list_completed

                # Обновляем прогресс-бар
                total_subtasks = len(task_subtasks)
                completed_count = sum(1 for subtask in task_subtasks if subtask.status == "Готово")

                # Логирование для отладки
                print(f"Задача: {task.taskname}, Общее количество подзадач: {total_subtasks}, Выполненные: {completed_count}")

                # Обновление значения прогресс-бара
                if total_subtasks > 0:
                    progress_bar.value = completed_count / total_subtasks 
                else:
                    progress_bar.value = 0

                # Добавляем подзадачи в соответствующие списки
                for subtask in task_subtasks:
                    if subtask.status == "В процессе":
                        subtask_row = create_subtask_container(subtask.id, task.id, subtask.subtaskname, process_list, test_list, completed_list, progress_bar)
                        process_list.controls.append(subtask_row)
                    elif subtask.status == "На проверке":
                        if admin_role:
                            subtask_row = create_subtask_container(subtask.id, task.id, subtask.subtaskname, process_list, test_list, completed_list, progress_bar)
                            test_list.controls.append(subtask_row)
                        else:
                            subtask_text_row = ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.YELLOW),
                                    ft.Text(subtask.subtaskname, size=16, width=240, color=ft.colors.WHITE)
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            )
                            test_list.controls.append(subtask_text_row)
                    elif subtask.status == "Готово":
                        subtask_compl_row = ft.Row(
                            controls=[
                                ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.GREEN),
                                ft.Text(subtask.subtaskname, size=16, width=240, color=ft.colors.WHITE)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        )
                        completed_list.controls.append(subtask_compl_row)

                my_task_list.controls.append(task_container)

        page.update()  # Обновляем страницу после загрузки задач

    def load_tasks():
        all_task_list.controls.clear()

        tasks = get_tasks()  # Получаем все задачи
        subtasks = get_subtasks()  # Получаем все подзадачи

        for task in tasks:

            if not any(container.task_id == task.id for container in all_task_list.controls):
                if task.status == "Выполнено":
                    continue

                progress_bar = create_progress_bar()    
                
                task_container = create_task_container(
                    task.id, task.taskname, confirm_name_task, open_task,
                    add_people, all_task_list, page, show_confirm_delete_task_dialog,
                    add_subtask, admin_role, show_responsible_users_dialog,
                    add_file, get_files, progress_bar
                )

                # Находим подзадачи для текущей задачи
                task_subtasks = [subtask for subtask in subtasks if subtask.id_task == task.id]

                process_list = task_container.in_all_task_list_process
                test_list = task_container.in_all_task_list_test
                completed_list = task_container.in_all_task_list_completed

                # Обновляем прогресс-бар
                total_subtasks = len(task_subtasks)
                completed_count = sum(1 for subtask in task_subtasks if subtask.status == "Готово")

                # Логирование для отладки
                print(f"Задача: {task.taskname}, Общее количество подзадач: {total_subtasks}, Выполненные: {completed_count}")

                # Обновление значения прогресс-бара
                if total_subtasks > 0:
                    progress_bar.value = completed_count / total_subtasks 
                else:
                    progress_bar.value = 0

                # Добавляем подзадачи в соответствующие списки
                for subtask in task_subtasks:
                    if subtask.status == "В процессе":
                        subtask_row = create_subtask_container(subtask.id, task.id, subtask.subtaskname, process_list, test_list, completed_list, progress_bar)
                        process_list.controls.append(subtask_row)
                    elif subtask.status == "На проверке":
                        
                        # Проверяем является ли пользователь администратором
                        # Если да, то создаем чекбокс
                        if admin_role:
                            subtask_row = create_subtask_container(subtask.id, task.id, subtask.subtaskname, process_list, test_list, completed_list, progress_bar)
                            test_list.controls.append(subtask_row)
                        # Если нет, то создаем строку с текстом
                        else:
                            subtask_text_row = ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.YELLOW),
                                    ft.Text(subtask.subtaskname, size=16, width=240, color=ft.colors.WHITE)
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            )
                            test_list.controls.append(subtask_text_row)
                    elif subtask.status == "Готово":
                        # Создаем строку для подзадачи и добавляем в список завершенных
                        subtask_compl_row = ft.Row(
                            controls=[
                                ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.GREEN),
                                ft.Text(subtask.subtaskname, size=16, width=240, color=ft.colors.WHITE)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        )
                        completed_list.controls.append(subtask_compl_row)

                all_task_list.controls.append(task_container)

        page.update()  # Обновляем страницу после загрузки задач

    def load_comp_tasks():
        completed_task_list.controls.clear()  # Очищаем текущий список выполненных задач

        tasks = get_tasks()  # Получаем все задачи
        subtasks = get_subtasks()  # Получаем все подзадачи

        for task in tasks:
            if task.status == "Выполнено":  # Проверяем статус задачи
                completed_list = ft.ListView(spacing=10, expand=True, padding=ft.padding.only(top=10, left=10))

                # Находим подзадачи для текущей задачи
                task_subtasks = [subtask for subtask in subtasks if subtask.id_task == task.id]

                # Добавляем подзадачи в список выполненных
                for subtask in task_subtasks:
                    if subtask.status == "Готово":
                        subtask_row = ft.Row(
                            controls=[
                                ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.GREEN),
                                ft.Text(subtask.subtaskname, size=16, width=240, color=ft.colors.WHITE)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        )
                        completed_list.controls.append(subtask_row)

                # Создаем контейнер для выполненной задачи
                completed_task_container = create_completed_task_container(
                    task.id,
                    task.taskname,
                    open_task,
                    completed_list,
                    page,
                    show_responsible_users_dialog,
                    get_files
                )

                # Добавляем выполненную задачу в список "Выполнено"
                completed_task_list.controls.append(completed_task_container)

        page.update()  # Обновляем страницу после загрузки задач


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
                    update_subtask_status(subtask_id, "На проверке")

                else:
                    subtask_text_row = ft.Row(
                        controls=[
                            ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.YELLOW),
                            ft.Text(name, size=16, width=240, color=ft.colors.WHITE)
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    )
                    test_list.controls.append(subtask_text_row)
                    update_subtask_status(subtask_id, "На проверке")
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
                update_subtask_status(subtask_id, "Готово")
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
        update_progress_bar(task_id, process_list, test_list, completed_list, all_task_list)

        page.update()  # Обновляем страницу после изменений

    def update_progress_bar(task_id, process_list, test_list, completed_list, all_task_list):
        total_subtasks = len(process_list.controls) + len(test_list.controls) + len(completed_list.controls)
        completed_count = len(completed_list.controls)

        # Обновление значения прогресс-бара
        if total_subtasks > 0:
            progress_value = completed_count / total_subtasks
        else:
            progress_value = 0

        # Обновляем прогресс-бар для текущей задачи
        for task_container in all_task_list.controls:
            if task_container.task_id == task_id:  # Найти соответствующий контейнер задачи
                task_container.progress_bar.value = progress_value  # Обновляем значение прогресс-бара

                # Проверяем, заполнен ли прогресс бар
                if progress_value == 1.0:  # Можно использовать '==' для точной проверки
                    print("Задача выполнена!")
                    update_task_status(task_id, "Выполнено")  # Обновляем статус задачи в базе данных
                    
                    print("Создание контейнера для выполненной задачи")
                    completed_task_container = create_completed_task_container(
                        task_id, 
                        task_container.title_task.value, 
                        open_task, 
                        completed_list,
                        page, 
                        show_responsible_users_dialog, 
                        get_files
                    )
                    print("Контейнер для выполненной задачи создан:", completed_task_container)

                    # Удаляем контейнер задачи из списка активных задач
                    all_task_list.controls.remove(task_container)  # Удаляем контейнер задачи

                    # Добавляем выполненную задачу в список "Выполнено"
                    completed_task_list.controls.append(completed_task_container)
                    print("Задача перемещена в список 'Выполнено'.")

                    page.update()  # Обновляем страницу после изменений
                break

        # Обновляем интерфейс прогресс-бара
        page.update()
    
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