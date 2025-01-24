import flet as ft

def home_page(page: ft.Page):
    page.title = "DOT SENSE"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 16
    page.bgcolor = "#669eff"  # Fondo de la pantalla

    # Títulos
    title = ft.Text("DOT SENSE", size=32, weight="bold", color="#FFFFFF")
    subtitle = ft.Text("Traductor de texto a braille", size=18, color="#FFFFFF")

    # Botón
    def on_button_click(e):
        page.go("/explore")  # Navegar a la página "explore"

    button = ft.ElevatedButton(
        text="Empezar",
        bgcolor="#e61548",  # Color del botón
        color="#FFFFFF",  # Color del texto del botón
        on_click=on_button_click,  # Acción del botón
        style=ft.ButtonStyle(
            padding={"top": 12, "bottom": 12, "left": 24, "right": 24},  # Espaciado
            shape=ft.RoundedRectangleBorder(radius=24),  # Bordes redondeados
        )
    )

    # Estructura de la página
    page.add(
        ft.Column(
            controls=[title, subtitle, button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=32,
        )
    )

