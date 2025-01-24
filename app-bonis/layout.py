import flet as ft
from app import home_page
from explore import explore_page
from upload import upload_page

def main(page: ft.Page):
    # Habilitar la navegación en la aplicación
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.add(ft.Text("Cargando..."))  # Texto temporal mientras se carga la página inicial
    page.go("/")  # Ir a la ruta inicial

# Función para manejar los cambios de ruta
def route_change(e):
    page = e.page
    print(f"Navegando a la ruta: {page.route}")  # Mensaje de depuración
    page.controls.clear()  # Limpiar controles de la página actual

    

    if page.route == "/":
        home_page(page)  # Cargar la página de inicio
    elif page.route == "/explore":
        explore_page(page)  # Cargar la página de exploración
    elif page.route == "/upload":
        upload_page(page)  # Cargar la página de carga
    else:
        page.add(ft.Text("Página no encontrada"))  # Ruta no válida

    page.update()  # Actualizar la página

# Función para manejar la pila de navegación (para retroceder)
def view_pop(e):
    page = e.page
    if len(page.views) > 1:
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

# Ejecuta la aplicación
ft.app(target=main)
