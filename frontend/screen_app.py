import flet as ft

def main_screen(page, login):
    
    # Создаем откидной контейнер
    collapsible_container = ft.Container(
        content=ft.Text("Логин: " + login),
        width=150,
        height=150,
        # #101318
        bgcolor=ft.colors.BLACK,  # Изменяем цвет контейнера
        padding=ft.padding.all(10),
        border_radius=ft.border_radius.all(3),
        visible=False,
    )
    
    def show_account(e):
        # Переключаем видимость откидного контейнера
        collapsible_container.visible = not collapsible_container.visible
        page.update()
    
    main_screen_content = ft.Column(
        [
            ft.Row(
                [
                    ft.Container(
                        content=ft.TextButton(
                            text="Личный кабинет",
                            icon=ft.icons.ACCOUNT_CIRCLE,
                            on_click=show_account
                        ),
                        alignment=ft.alignment.top_right,
                        padding=ft.padding.only(right=10),
                    ),
                ],
                alignment=ft.MainAxisAlignment.END  
            ),
            # Добавляем откидной контейнер под кнопкой
            ft.Container(
                content=collapsible_container,
                alignment=ft.alignment.top_right, 
                padding=ft.padding.only(right=10) 
            )
        ],
        expand=True  # Заполнение экрана контейнером
    )
    
    page.add(main_screen_content)
