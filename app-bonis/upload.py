import flet as ft
from firebase_config import get_bucket, obtener_url_archivo
from procesamiento import procesar_desde_url
def upload_page(page: ft.Page):
    page.title = "Archivo Subido"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Recuperar el nombre del archivo desde el almacenamiento local
    archivo_nombre = page.client_storage.get("uploaded_file") or "Archivo desconocido"

    bucket = get_bucket()
    archivo_url = obtener_url_archivo(bucket, archivo_nombre)
    extension = archivo_nombre.split('.')[-1].lower() 
    print(extension)
    if archivo_url:
        # Procesar el archivo directamente desde la URL
        text, braille, angulos = procesar_desde_url(archivo_url,archivo_nombre)

        # Mostrar resultados en la interfaz
        if text and braille and angulos:
            page.add(
                ft.Column(
                    [
                        ft.Text("Archivo procesado con éxito.", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Nombre del archivo: {archivo_nombre}", size=18),
                        ft.Text(f"Texto detectado: {text}"),
                        ft.Text(f"Texto en Braille: {braille}"),
                        ft.Text(f"Ángulos enviados al ESP32: {angulos}"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                )
            )
        else:
            page.add(ft.Text("Error al procesar el archivo.", color="red"))
    else:
        page.add(ft.Text("Error al obtener la URL del archivo.", color="red"))

    page.update()


