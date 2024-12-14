import asyncio
import flet as ft


# Экран регистрации/авторизации
def create_input_login(validate):
    user_login = ft.TextField(label="Логин", width=300, on_change=validate)
    return user_login

def create_input_pass(validate):
    user_pass = ft.TextField(label="Пароль", width=300, on_change=validate, password=True)
    return user_pass

def create_btn_reg(register):
    btn_reg = ft.CupertinoFilledButton(text="Зарегистрироваться", width=300, height=50, on_click=register, disabled=True)
    return btn_reg

def create_btn_auth(auth):
    btn_auth = ft.CupertinoFilledButton(text="Авторизоваться", width=300, height=50, on_click=auth, disabled=True)
    return btn_auth

def create_sign_in_btn(show_sign_in):
    sign_in_btn = ft.TextButton("Авторизоваться", on_click=lambda e: show_sign_in(), style=ft.ButtonStyle(color=ft.colors.BLUE))
    return sign_in_btn

def create_sign_up_button(show_sign_up):
    sign_up_btn = ft.TextButton("Зарегистрироваться", on_click=lambda e: show_sign_up(), style=ft.ButtonStyle(color=ft.colors.BLUE))
    return sign_up_btn

def create_reg_panel(user_login, user_pass, btn_registered, already_registered_text, sign_in_button):
    panel_register = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Регистрация"),
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
                        padding=ft.padding.only(left=65),
                    ),
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    return panel_register

def create_auth_panel(user_login, user_pass, btn_auth, already_auth_text, sign_up_button):
    panel_auth = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Авторизация"),
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
                        padding=ft.padding.only(left=55),
                    ),
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    return panel_auth


# Основной экран приложения

def create_input_task(search_task):
    input_task = ft.TextField(
        label="Поиск",
        hint_text="Поиск задачи",
        text_size=14,
        border_color=ft.colors.WHITE,
        width=290,
        color="#a0cafd",
        max_lines=1,
        prefix_icon=ft.icons.SEARCH,
        on_change=lambda e: search_task(e.control.value),
    )
    return input_task

def create_my_task_btn(my_task_app):
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
    return my_task_button

def create_all_task_btn(all_task_app):
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
    return all_task_button

def create_completed_btn(done_app):
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
    return completed_button

def create_account_btn():
    account_button = ft.Row(
        [
            ft.Icon(ft.icons.ACCOUNT_CIRCLE),
            ft.Text("Личный кабинет", weight=ft.FontWeight.BOLD, color="#a0cafd"),
            ft.Icon(ft.icons.ARROW_DROP_DOWN),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    return account_button

def create_edit_btn():
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
    return edit_button

def create_exit_btn():
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
    return exit_button

def create_profile_dialog(close_icon, login_tile_container, password_tile_container, edit_button, exit_button):
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
    return profile_dialog

def create_responsible_person_dialog(get_responsible_users, task_id, get_users, close_icon):
    # Получаем логины пользователей, связанных с задачей
    responsible_users = get_responsible_users(task_id)
    users = [user.username for user in get_users() if user.id in responsible_users]
    
    # Создаем список логинов
    users_list = ft.ListView(spacing=15, padding=ft.padding.all(10), expand=True)
    for user in users:
        users_list.controls.append(ft.ListTile(
            leading=ft.Icon(ft.icons.PERSON),
            title=ft.Text(user, size=25)
        ))
    
    responsible_users_dialog = ft.AlertDialog(
        modal=False,
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [close_icon],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    users_list
                ],
            ),
            width=400,
            height=400,
        )
    )
    
    return responsible_users_dialog

def create_add_person_dialog(get_users, close_icon, page, insert_person, task_id, get_associated_users, remove_user_from_task):
    users = get_users()
    user_list = ft.ListView(spacing=15, padding=ft.padding.all(10), expand=True)
    
    associated_users = get_associated_users(task_id)
    
    for user in users:
        icon_button = ft.IconButton(icon=ft.icons.ADD, icon_color=ft.colors.GREEN, tooltip="Добавить")
        icon_button.clicked = False  
        
        if user[0] in associated_users:
            icon_button.icon = ft.icons.CHECK_CIRCLE
            icon_button.tooltip = "Удалить"
            icon_button.clicked = True
        
        def create_toggle_icon(icon_button, user):
            def toggle_icon(e):
                if icon_button.clicked:
                    icon_button.icon = ft.icons.ADD
                    icon_button.tooltip = "Добавить"
                    print(f"Удален пользователь {user[1]}")
                    remove_user_from_task(task_id, user[0])
                else:
                    icon_button.icon = ft.icons.CHECK_CIRCLE
                    icon_button.tooltip = "Удалить"
                    print(f"Добавлен пользователь {user[1]}")
                    insert_person(task_id, user[0])
                icon_button.clicked = not icon_button.clicked  
                page.update()  
            return toggle_icon

        icon_button.on_click = create_toggle_icon(icon_button, user)

        user_list.controls.append(ft.ListTile(
            leading=icon_button,
            title=ft.Text(user[1], size=25)
        ))

    add_person_dialog = ft.AlertDialog(
        modal=False,
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [close_icon],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    user_list
                ]
            ),
            width=400,
            height=400,
        )
    )
    return add_person_dialog

def create_update_profile_dialog(close_icon, new_username_input, new_password_input, save_button):
    update_dialog = ft.AlertDialog(
        modal=False,
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [close_icon],
                                    alignment=ft.MainAxisAlignment.END
                                ),
                                ft.Text("Редактирование профиля", size=24, weight=ft.FontWeight.BOLD),
                                ft.Text("Введите новые данные", size=18),
                            ],
                            spacing=10,
                        ),
                        padding=ft.padding.all(10),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                new_username_input,
                                new_password_input,
                                save_button
                            ],
                            spacing=15,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.all(10),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            width=340,
            height=350,
            border_radius=10,
        )
    )
    return update_dialog

def create_confirm_delete_task_dialog(delete_task, task_id, task_container, all_task_list, page, close_icon):
    confirm_delete_task_dialog = ft.AlertDialog(
        modal=False,
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Container(  # Container for text elements
                        content=ft.Column(
                            [
                                ft.Text("Удаление задачи", size=24, weight=ft.FontWeight.BOLD),
                                ft.Text("Вы уверены, что хотите удалить эту задачу?", size=18),
                            ],
                            spacing=10,
                        ),
                        padding=ft.padding.all(10),
                    ),
                    ft.Container(  # Container for buttons
                        content=ft.Row(
                            [
                                ft.CupertinoFilledButton("ДА", expand=True, on_click=lambda e: delete_task(task_id, task_container, all_task_list, page, confirm_delete_task_dialog)),
                                ft.CupertinoFilledButton("НЕТ", expand=True, on_click=lambda e: close_icon.on_click(e)),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.all(10),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Add space between the two containers
            ),
            width=400,
            height=180,
            border_radius=10,
        ),
    )
    return confirm_delete_task_dialog

def create_file_container(task_id, get_files):
    file_button = ft.TextButton(
        content=ft.Row(
            [
                ft.Text("Загруженные файлы"),
                ft.Icon(ft.icons.FOLDER)
            ],
            width=175,
        ),
        on_click=lambda e: get_files(task_id, e),
    )

    file_container = ft.Container(
        content=file_button,
        padding=ft.padding.all(10),
    )

    return file_container

def create_files_dialog(task_id, download_file, get_files_by_task, close_icon, delete_file, page):
    files_list = ft.ListView(spacing=15, padding=ft.padding.all(10), expand=True)

    files_dialog = ft.AlertDialog(
        modal=False,
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [close_icon],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    files_list
                ],
            ),
            width=400,
            height=400,
        )
    )

    # Функция для обновления списка файлов
    def update_file_list():
        files_list.controls.clear()  # Очищаем текущий список
        files = get_files_by_task(task_id)  # Получаем обновленный список файлов
        for file in files:
            files_list.controls.append(ft.ListTile(
                title=ft.Text(file.file_name),
                leading=ft.Icon(ft.icons.FILE_PRESENT),
                trailing=ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color=ft.colors.RED,
                    tooltip="Удалить файл",
                    on_click=lambda e, file_id=file.id: delete_and_update(file_id)  # Передаем правильный file_id
                ),
                on_click=lambda e, file_data=file.file_data, file_name=file.file_name: download_file(file_data, file_name)
            ))
        page.update()  # Обновляем ListView после добавления новых элементов

    # Функция для удаления файла и обновления списка
    def delete_and_update(file_id):
        delete_file(file_id)  # Удаляем файл из базы данных
        update_file_list()  # Обновляем список файлов в интерфейсе

    # Обновляем список файлов после открытия диалога
    update_file_list()

    return files_dialog

def create_progress_bar():
    progress_bar = ft.ProgressBar(
        width=200, 
        height=10, 
        color=ft.colors.GREEN, 
        value=0, 
        bar_height=10, 
        border_radius=10
        )

    return progress_bar

def create_my_task_container(task_id, task_name, open_task, show_responsible_users_dialog, add_file,
                             get_files, progress_bar):
    
    title_task = ft.TextField(value=task_name, text_size=22, color=ft.colors.BLACK, read_only=True, border_width=0, width=None, max_lines=2, expand=True)
    
    in_all_task_list_process = ft.ListView(spacing=10, expand=True, padding=ft.padding.only(top=10, left=10))
    in_all_task_list_test = ft.ListView(spacing=10, expand=True, padding=ft.padding.only(top=10, left=10))
    in_all_task_list_completed = ft.ListView(spacing=10, expand=True, padding=ft.padding.only(top=10, left=10))

    file_container = create_file_container(task_id, get_files)
    # Создаем кнопку загрузки файла
    btn_upload_file = ft.TextButton(
        content=ft.Row(
            [
                ft.Text("Прикрепить файл"),
                ft.Icon(ft.icons.UPLOAD_FILE)
            ],
        ),
        width=175,
        on_click=lambda e: add_file(file_container, task_id, e), 
    )
    
    subtask_container_process = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("В ПРОЦЕССЕ", size=22, color=ft.colors.WHITE)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border=ft.border.only(bottom=ft.border.BorderSide(1.5)),
                    animate_opacity=900,  # добавляем анимацию прозрачности
                    opacity=1,  # начальная прозрачность
                ),
                in_all_task_list_process,
                ft.Container(
                    content=ft.Column(
                        [
                            btn_upload_file
                        ]
                    ),
                    padding=ft.padding.only(left=10, bottom=10),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        width=280,
        height=375,
        bgcolor="#111418",  # Измените цвет фона на светло-голубой
        border=ft.border.all(1.5),
        border_radius=10,
        animate_opacity=900,  # добавляем анимацию прозрачности
        opacity=1,  # начальная прозрачность
    )
    
    subtask_container_test = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("НА ПРОВЕРКЕ", size=22, color=ft.colors.WHITE)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border=ft.border.only(bottom=ft.border.BorderSide(1.5)),
                    animate_opacity=900,  # добавляем анимацию прозрачности
                    opacity=1,  # начальная прозрачность
                ),
                in_all_task_list_test,
                file_container
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        width=280,
        height=375,
        bgcolor="#111418",  # Измените цвет фона на светло-голубой
        border=ft.border.all(1.5),
        border_radius=10,
        animate_opacity=900,  # добавляем анимацию прозрачности
        opacity=1,  # начальная прозрачность
    )
    
    subtask_container_completed = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("ГОТОВО", size=22, color=ft.colors.WHITE)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border=ft.border.only(bottom=ft.border.BorderSide(1.5)),
                    animate_opacity=900,  # добавляем анимацию прозрачности
                    opacity=1,  # начальная прозрачность
                ),
                in_all_task_list_completed,
            ],
            spacing=10,
        ),
        width=280,
        height=375,
        bgcolor="#111418",  # Измените цвет фона на светло-голубой
        border=ft.border.all(1.5),
        border_radius=10,
        animate_opacity=900,  # добавляем анимацию прозрачности
        opacity=1,  # начальная прозрачность
    )
    
    my_task_container = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        title_task,
                    ],
                ),
                ft.Row( 
                    [
                        ft.TextButton(
                            content=ft.Row(
                                [
                                    ft.Text("Посмотреть все", color = ft.colors.GREEN),
                                    ft.Icon(ft.icons.ARROW_DROP_DOWN, color = ft.colors.GREEN)
                                ],
                            ),
                            on_click=lambda e: open_task(my_task_container, e),
                        ),
                        ft.TextButton(
                            content=ft.Row(
                                [
                                    ft.Text("Посмотреть исполнителей"),
                                    ft.Icon(ft.icons.PEOPLE)
                                ],
                            ),
                            on_click=lambda e: show_responsible_users_dialog(task_id, e),
                        ),

                        progress_bar,
                    ],
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            subtask_container_process, 
                            subtask_container_test,
                            subtask_container_completed 
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
    my_task_container.task_id = task_id

    my_task_container.in_all_task_list_process = in_all_task_list_process
    my_task_container.in_all_task_list_test = in_all_task_list_test
    my_task_container.in_all_task_list_completed = in_all_task_list_completed
    my_task_container.progress_bar = progress_bar
    my_task_container.title_task = title_task

    my_task_container.is_open = False  # добавляем атрибут is_open
    
    return my_task_container

def create_task_container(task_id, task_name, confirm_name_task, open_task, add_people, 
                          all_task_list, page, show_confirm_delete_task_dialog, add_subtask, 
                          is_admin, show_responsible_users_dialog, add_file, get_files, progress_bar):

    title_task = ft.TextField(value=task_name, text_size=22, color=ft.colors.BLACK, read_only=False, border_width=0, width=None, max_lines=2, expand=True)
    title_task_user = ft.TextField(value=task_name, text_size=22, color=ft.colors.BLACK, read_only=True, border_width=0, width=None, max_lines=2, expand=True)
    
    in_all_task_list_process = ft.ListView(spacing=10, expand=True, padding=ft.padding.only(top=10, left=10))
    in_all_task_list_test = ft.ListView(spacing=10, expand=True, padding=ft.padding.only(top=10, left=10))
    in_all_task_list_completed = ft.ListView(spacing=10, expand=True, padding=ft.padding.only(top=10, left=10))

    # Создаем контейнер файла
    file_container = create_file_container(task_id, get_files)
    
    # Добавляем кнопку добавления подзадачи только для администраторов
    btn_add_subtask = ft.TextButton(
        content=ft.Row(
            [
                ft.Text("Добавить подзадачу"),
                ft.Icon(ft.icons.ADD)
            ],
        ),
        width=190,
        on_click=lambda e: add_subtask(task_id, None, in_all_task_list_process, in_all_task_list_test, in_all_task_list_completed, progress_bar, e),
    ) if is_admin else None  # Условие для отображения кнопки

    # Создаем кнопку загрузки файла
    btn_upload_file = ft.TextButton(
        content=ft.Row(
            [
                ft.Text("Прикрепить файл"),
                ft.Icon(ft.icons.UPLOAD_FILE)
            ],
        ),
        width=175,
        on_click=lambda e: add_file(file_container, task_id, e),  # Привязка к кнопке
    )

    subtask_container_process = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("В ПРОЦЕССЕ", size=22, color=ft.colors.WHITE)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border=ft.border.only(bottom=ft.border.BorderSide(1.5)),
                    animate_opacity=900,  # добавляем анимацию прозрачности
                    opacity=1,  # начальная прозрачность
                ),
                in_all_task_list_process,
                ft.Container(
                    content=ft.Column(
                        [
                            btn_add_subtask if btn_add_subtask is not None else ft.Container(),  # Проверка на None
                            btn_upload_file
                        ]
                    ),
                    padding=ft.padding.only(left=10, bottom=10),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        width=280,
        height=380,
        bgcolor="#111418",  # Измените цвет фона на светло-голубой
        border=ft.border.all(1.5),
        border_radius=10,
        animate_opacity=900,  # добавляем анимацию прозрачности
        opacity=1,  # начальная прозрачность
    )

    subtask_container_test = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("НА ПРОВЕРКЕ", size=22, color=ft.colors.WHITE)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border=ft.border.only(bottom=ft.border.BorderSide(1.5)),
                    animate_opacity=900,  # добавляем анимацию прозрачности
                    opacity=1,  # начальная прозрачность
                ),
                in_all_task_list_test,
                file_container,  # Используем file_container для отображения имени файла
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        width=280,
        height=380,
        bgcolor="#111418",  # Измените цвет фона на светло-голубой
        border=ft.border.all(1.5),
        border_radius=10,
        animate_opacity=900,  # добавляем анимацию прозрачности
        opacity=1,  # начальная прозрачность
    )

    
    subtask_container_completed = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row (
                        [
                            ft.Text("ГОТОВО", size=22, color=ft.colors.WHITE)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border=ft.border.only(bottom=ft.border.BorderSide(1.5)),
                    animate_opacity=900,  # добавляем анимацию прозрачности
                    opacity=1,  # начальная прозрачность
                ),
                in_all_task_list_completed,
            ],
            spacing=10,
        ),
        width=280,
        height=380,
        bgcolor="#111418",  # Измените цвет фона на светло-голубой
        border=ft.border.all(1.5),
        border_radius=10,
        animate_opacity=900,  # добавляем анимацию прозрачности
        opacity=1,  # начальная прозрачность
    )
    
    if is_admin:
        btn_add_people = ft.TextButton(
            content=ft.Row(
                [
                    ft.Text("Добавить исполнителя"),
                    ft.Icon(ft.icons.PERSON_ADD)
                ],
            ),
            on_click=lambda e: add_people(task_id, e),
        )
        
        all_task_container = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            title_task,
                            ft.IconButton(
                                ft.icons.CHECK, 
                                icon_color=ft.colors.GREEN, 
                                tooltip="Сохранить изменения", 
                                on_click= lambda e: asyncio.run(confirm_name_task(title_task.value, task_id, e))
                                )
                        ],
                    ),
                    ft.Row(  # Добавляем обе кнопки в один Row
                        [
                            ft.TextButton(
                                content=ft.Row(
                                    [
                                        ft.Text("Посмотреть все", color = ft.colors.GREEN),
                                        ft.Icon(ft.icons.ARROW_DROP_DOWN, color = ft.colors.GREEN)
                                    ],
                                ),
                                on_click=lambda e: open_task(all_task_container, e),
                            ),
                            btn_add_people,
                            
                            ft.TextButton(
                                content=ft.Row(
                                    [
                                        ft.Text("Удалить задачу", color = ft.colors.RED),
                                        ft.Icon(ft.icons.DELETE, color = ft.colors.RED)
                                    ],
                                ),
                                on_click=lambda e: show_confirm_delete_task_dialog(task_id, e, all_task_container, all_task_list, page),
                            ),

                            progress_bar
                        ],
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                subtask_container_process, 
                                subtask_container_test,
                                subtask_container_completed 
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
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
    else:
        all_task_container = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            title_task_user
                        ],
                    ),
                    ft.Row(  # Добавляем обе кнопки в один Row
                        [
                            ft.TextButton(
                                content=ft.Row(
                                    [
                                        ft.Text("Посмотреть все", color = ft.colors.GREEN),
                                        ft.Icon(ft.icons.ARROW_DROP_DOWN, color = ft.colors.GREEN)
                                    ],
                                ),
                                on_click=lambda e: open_task(all_task_container, e),
                            ),
                            ft.TextButton(
                                content=ft.Row(
                                    [
                                        ft.Text("Посмотреть исполнителей"),
                                        ft.Icon(ft.icons.PEOPLE)
                                    ],
                                ),
                                on_click=lambda e: show_responsible_users_dialog(task_id, e),
                            ),
                            
                            progress_bar,
                        ],
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                subtask_container_process, 
                                subtask_container_test,
                                subtask_container_completed 
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
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
    
    all_task_container.in_all_task_list_process = in_all_task_list_process
    all_task_container.in_all_task_list_test = in_all_task_list_test
    all_task_container.in_all_task_list_completed = in_all_task_list_completed
    all_task_container.progress_bar = progress_bar
    all_task_container.title_task = title_task
    
    all_task_container.task_id = task_id
    all_task_container.is_open = False  # добавляем атрибут is_open
    return all_task_container

def create_completed_task_container(task_id, task_name, open_task, completed_list,
                                    page, show_responsible_users_dialog, get_files, completed_task_list, show_confirm_delete_task_dialog):

    title_task = ft.TextField(value=task_name, text_size=22, color=ft.colors.BLACK, read_only=True, border_width=0, width=None, max_lines=2, expand=True)
    
    progress_bar = ft.ProgressBar(width=200, height=10, color=ft.colors.GREEN, value=0, bar_height=10, border_radius=10)
    progress_bar.value = 1

    in_comp_task_list_test = ft.ListView(spacing=10, expand=True, padding=ft.padding.only(top=10, left=10))

    # Создаем контейнер файла
    file_container = create_file_container(task_id, get_files)

    subtask_container_process = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("В ПРОЦЕССЕ", size=22, color=ft.colors.WHITE)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border=ft.border.only(bottom=ft.border.BorderSide(1.5)),
                    animate_opacity=900,  # добавляем анимацию прозрачности
                    opacity=1,  # начальная прозрачность
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        width=280,
        height=380,
        bgcolor="#111418",  # Измените цвет фона на светло-голубой
        border=ft.border.all(1.5),
        border_radius=10,
        animate_opacity=900,  # добавляем анимацию прозрачности
        opacity=1,  # начальная прозрачность
    )

    subtask_container_test = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("НА ПРОВЕРКЕ", size=22, color=ft.colors.WHITE)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border=ft.border.only(bottom=ft.border.BorderSide(1.5)),
                    animate_opacity=900,  # добавляем анимацию прозрачности
                    opacity=1,  # начальная прозрачность
                ),
                in_comp_task_list_test,
                file_container,  # Используем file_container для отображения файлов
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        width=280,
        height=380,
        bgcolor="#111418",  # Измените цвет фона на светло-голубой
        border=ft.border.all(1.5),
        border_radius=10,
        animate_opacity=900,  # добавляем анимацию прозрачности
        opacity=1,  # начальная прозрачность
    )

    
    subtask_container_completed = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row (
                        [
                            ft.Text("ГОТОВО", size=22, color=ft.colors.WHITE)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border=ft.border.only(bottom=ft.border.BorderSide(1.5)),
                    animate_opacity=900,  # добавляем анимацию прозрачности
                    opacity=1,  # начальная прозрачность
                ),
                completed_list,
            ],
            spacing=10,
        ),
        width=280,
        height=380,
        bgcolor="#111418",  # Измените цвет фона на светло-голубой
        border=ft.border.all(1.5),
        border_radius=10,
        animate_opacity=900,  # добавляем анимацию прозрачности
        opacity=1,  # начальная прозрачность
    )
    
    comp_task_container = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        title_task,   
                    ],
                ),
                ft.Row(  # Добавляем обе кнопки в один Row
                    [
                        ft.TextButton(
                            content=ft.Row(
                                [
                                    ft.Text("Посмотреть все", color = ft.colors.GREEN),
                                    ft.Icon(ft.icons.ARROW_DROP_DOWN, color = ft.colors.GREEN)
                                ],
                            ),
                            on_click=lambda e: open_task(comp_task_container, e),
                        ),      

                        ft.TextButton(
                                content=ft.Row(
                                    [
                                        ft.Text("Посмотреть исполнителей"),
                                        ft.Icon(ft.icons.PEOPLE)
                                    ],
                                ),
                                on_click=lambda e: show_responsible_users_dialog(task_id, e),
                            ),      

                        ft.TextButton(
                                content=ft.Row(
                                    [
                                        ft.Text("Удалить задачу", color = ft.colors.RED),
                                        ft.Icon(ft.icons.DELETE, color = ft.colors.RED)
                                    ],
                                ),
                                on_click=lambda e: show_confirm_delete_task_dialog(task_id, e, comp_task_container, completed_task_list, page),
                            ),

                        progress_bar,
                    ],
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            subtask_container_process, 
                            subtask_container_test,
                            subtask_container_completed 
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
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
    
    comp_task_container.task_id = task_id
    comp_task_container.is_open = False  # добавляем атрибут is_open

    return comp_task_container

def create_header_container(title_app, profile_button):
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
    return header_container

def create_nav_container(input_task, my_task_button, all_task_button, completed_button):
    navigation_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(content=input_task, padding=ft.padding.only(top=20)),
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
        border=ft.Border(right=ft.BorderSide(1)),
    )
    return navigation_container

def create_panel_my_task(my_task_list, load_my_tasks):
    
    btn_update = ft.IconButton(
        icon=ft.icons.UPDATE,
        tooltip="Обновить",
        on_click=lambda e: load_my_tasks()
    )
    
    panel_my_tasks = ft.Container(
        content=ft.Column(  
            [   
                ft.Row(
                    [
                        ft.Text("Мои задачи", style="headlineMedium"),
                        btn_update
                    ],
                    spacing=10,
                ),
                
                ft.Container(
                    content=my_task_list,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            expand=True,
        ),
    )
    return panel_my_tasks

def create_panel_all_tasks(add_task, all_task_list, is_admin): 
    panel_all_tasks = ft.Container(
        content=ft.Column(  
            [   
                ft.Row(
                    [
                        ft.Text("Все задачи", style="headlineMedium"),
                        # Добавляем кнопку "Добавить задачу" только для администраторов
                        ft.IconButton(ft.icons.ADD_TASK, icon_color=ft.colors.GREEN, tooltip="Добавить задачу", on_click=add_task) if is_admin else ft.Container()  # Условие для отображения кнопки
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
    )
    return panel_all_tasks

def create_panel_done(completed_task_list, load_comp_tasks):

    btn_update = ft.IconButton(
        icon=ft.icons.UPDATE,
        tooltip="Обновить",
        on_click=lambda e: load_comp_tasks()
    )
    
    panel_done = ft.Container(
        content=ft.Column(  
            [   
                ft.Row(
                    [
                        ft.Text("Выполнено", style="headlineMedium"),
                        btn_update
                    ],
                    spacing=10,
                ),
                completed_task_list
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            expand=True,
        ),
    )
    return panel_done

def create_screen_app(header_container, navigation_container, main_container):
    screen_app = ft.Column(
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
    return screen_app