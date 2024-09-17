import flet as ft

def main_screen(page, login):
    
    login_tile_container = ft.Container(
        content=ft.ListTile(
            title=ft.Text(login, color=ft.colors.WHITE),
            subtitle=ft.Text("Ваш логин", color=ft.colors.WHITE70),
        ),
        padding=ft.padding.only(left=5),
        alignment=ft.alignment.center_right,
    )
    
    # Создаем кнопку "Редактировать"
    edit_button = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(ft.icons.SETTINGS, color=ft.colors.WHITE),
                ft.Text("Редактировать", color=ft.colors.WHITE)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.TRANSPARENT,
            overlay_color=ft.colors.TRANSPARENT
        ),
    )

    edit_button_container = ft.Container(
        content=edit_button,
        padding=ft.padding.only(right=10), 
    )

    # Создаем контент для раскрывающейся части
    content = ft.Column(
        [
            login_tile_container,
            edit_button_container
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
    )

    # Создаем кнопку "Личный кабинет"
    account_button = ft.Row(
        [
            ft.Icon(ft.icons.ACCOUNT_CIRCLE, color=ft.colors.WHITE),
            ft.Text("Личный кабинет", color=ft.colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Основной контейнер, который включает в себя кнопку и раскрывающуюся часть
    main_container = ft.Container(
        content=ft.Column(
            [
                account_button,
                content,
            ],
            spacing=10,
        ),
        width=200,
        height=40,  # Начальная высота (высота кнопки)
        bgcolor="#1e88e5",
        border_radius=ft.border_radius.all(15),
        padding=ft.padding.all(10),
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
    )

    def toggle_container(e):
        if main_container.height == 40:
            main_container.height = 180  # Увеличиваем высоту для новой кнопки
        else:
            main_container.height = 40  # Высота только кнопки
        page.update()

    main_container.on_click = toggle_container

    def edit_profile(e):
        print("Редактирование профиля")
        # Здесь можно добавить логику для редактирования профиля

    edit_button.on_click = edit_profile

    main_screen_content = ft.Column(
        [
            ft.Container(
                content=main_container,
                alignment=ft.alignment.top_right,
                padding=ft.padding.only(right=10)
            ),
        ],
        expand=True  # Заполнение экрана контейнером
    )
    
    page.add(main_screen_content)