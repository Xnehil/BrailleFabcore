import flet as ft
from firebase_config import get_bucket

# Inicializamos el bucket de Firebase
storage = get_bucket()

def explore_page(page: ft.Page):
    page.title = "Subir Archivo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Texto de estado
    status_text = ft.Text("")  # Texto para mostrar el estado de la carga

    # Función para manejar la carga de archivos a Firebase Storage
    def cargar_archivo(e):
        if file_picker.result and file_picker.result.files:
            archivo = file_picker.result.files[0]  # Tomamos el primer archivo
            archivo_nombre = archivo.name

            try:
                # Subimos el archivo a Firebase Storage
                #bucket = storage.bucket()
                blob = storage.blob(f"BRAILLE/{archivo_nombre}")
                with open(archivo.path, "rb") as f:
                    blob.upload_from_file(f)

                status_text.value = f"Archivo '{archivo_nombre}' subido con éxito."
                page.client_storage.set("uploaded_file", archivo_nombre)  # Guardar en almacenamiento local
                page.go("/upload")  # Navegar a la página de upload
                #page.update()
            except Exception as ex:
                status_text.value = f"Error al subir el archivo: {str(ex)}"
        else:
            status_text.value = "No se seleccionó ningún archivo."
        page.update()

    # Crear el selector de archivos
    file_picker = ft.FilePicker(on_result=cargar_archivo)

    # Agregar el FilePicker como overlay
    page.overlay.append(file_picker)

    # Botón para abrir el FilePicker
    seleccionar_archivo_btn = ft.ElevatedButton(
        "Seleccionar Archivo",
        on_click=lambda _: file_picker.pick_files(allow_multiple=False),
    )

    # Diseño de la página
    page.add(
        ft.Column(
            [
                ft.Text("Subir Archivo a Firebase", size=24, weight=ft.FontWeight.BOLD),
                seleccionar_archivo_btn,
                status_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )
