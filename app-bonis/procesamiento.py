import requests 
#import pytesseract
from io import BytesIO
from PIL import Image
import textoABraille as tb
import pipeline as pl

def send_signals_to_esp32(angulos):
    # Convert Braille text to servo motor angles
    url = "http://192.168.18.212/paqueteAngulos"
    
    # Cada paquete de ágnulso viene como (ángulo1, ángulo2)
    stringToSend ="["
    angulosSet = []
    angulosSet += [f"({angulo[0]},{angulo[1]})" for angulo in angulos]
    for i in range(len(angulosSet)):
        stringToSend += angulosSet[i]
        if i != len(angulosSet)-1:
            stringToSend += ","
    stringToSend += "]"
    payload =  {"angulos": stringToSend}
    
    try:
        # POST a la URL con los ángulos
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            print(f"Se enviaron los ángulos: {payload}")
        else:
            print(f"No se pudieron enviar los ángulos:  {payload}")
    except requests.exceptions.RequestException as e:
        print(f"Error enviando los ángulos: {e}")


def procesar_desde_url(url,archivo_nombre):
    try:
        # Descargar el archivo desde la URL
        response = requests.get(url)
        if response.status_code == 200:
            # Abrir la imagen directamente desde la respuesta en memoria
            extension = archivo_nombre.split('.')[-1].lower() 

            # Verificar el tipo de archivo (imagen o PDF)
            if extension in ['png', 'jpg', 'jpeg', 'bmp']:
                # Procesar imagen
                image = Image.open(BytesIO(response.content))
                text = pl.process_image(image)  # Llamar a la función de pipeline para obtener el texto procesado
            elif extension == 'pdf':
                # Procesar PDF
                text = pl.process_pdf(url)
            else:
                print("Formato de archivo no soportado.")
                return None, None, None

            # Convertir el texto a Braille y señales
            braille = tb.convertirTextoABraille(text)
            seniales = tb.convertirASeñales(text)
            angulos = tb.convertirAAngulos(text)

            print(f"Texto detectado: {text}")
            print(f"Braille: {braille}")
            print(f"Señales: {[format(s, '06b') for s in seniales]}")
            print(f"Ángulos: {angulos}")

            # Enviar los ángulos al ESP32
            send_signals_to_esp32(angulos)

            return text, braille, angulos
        else:
            print(f"Error al descargar el archivo desde la URL: {response.status_code}")
            return None, None, None
    except Exception as e:
        print(f"Error procesando el archivo desde la URL: {e}")
        return None, None, None
