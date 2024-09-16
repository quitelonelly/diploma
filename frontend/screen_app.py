import flet as ft

def main_screen(page):
    main_screen_content = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("ОСНОВНОЙ ЭКРАН!"),
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    page.add(main_screen_content)
