import cv2
import pytesseract
import textoABraille as tb
import numpy as np
import pymupdf
from PIL import Image

def convertirImagen(imagen, debug=False):
    # Convertir imagen a escala de grises
    imagen = preprocesarImagen(imagen)
    #Sacar el texto de la imagen
    texto = pytesseract.image_to_string(imagen)
    # Texto a braille
    if debug:
        print("Texto conseguido de la imagen: ", texto)
    braille = tb.convertirTextoABraille(texto)
    return braille

def preprocesarImagen(imagen, resize_factor=4, extension='png'):

    print(imagen.shape)
    if len(imagen.shape) == 2:  # Si es una imagen de un solo canal (escala de grises)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_GRAY2BGR)  # Convertir a 3 canales (RGB)

    norm_img = np.zeros((imagen.shape[0], imagen.shape[1]))
    imagen = cv2.normalize(imagen, norm_img, 0, 255, cv2.NORM_MINMAX)

    # Solo invertir la imagen si el promedio de brillo es menor a 128 (imagen oscura)
    avg_brightness = np.mean(imagen)
    if avg_brightness < 128:
        imagen = cv2.bitwise_not(imagen)

    if extension.lower() in ['png', 'bmp']:
        imagen = cv2.resize(imagen, (imagen.shape[1] * resize_factor, imagen.shape[0] * resize_factor))
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((3, 3), np.uint8)
        imagen = cv2.dilate(imagen, kernel, iterations=1)
        imagen = cv2.erode(imagen, kernel, iterations=1)
        imagen = cv2.adaptiveThreshold(imagen, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    elif extension.lower() in ['jpg', 'jpeg']:
        imagen = cv2.resize(imagen, (imagen.shape[1] * resize_factor, imagen.shape[0] * resize_factor))
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        imagen = cv2.GaussianBlur(imagen, (3, 3), 0)
        _, imagen = cv2.threshold(imagen, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    
    

    return imagen

def process_image(image):
    # Open the image using PIL
    #image = Image.open(file_path)
    image = np.array(image)
    #extension = file_path.split('.')[-1]
    processed_image = preprocesarImagen(image, resize_factor=4)

    cv2.imwrite('processed_image.png', processed_image)
    text = pytesseract.image_to_string(processed_image)
    return text

def process_pdf(file_path):
    doc = pymupdf.open(file_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text()
        if page_text.strip():
            # If text is found, add it to the text variable
            text += page_text
        else:
            # If no text is found, use OCR
            pix = page.get_pixmap()
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            image = np.array(image)
            processed_image = preprocesarImagen(image)
            cv2.imwrite('processed_image.png', processed_image)
            text += pytesseract.image_to_string(processed_image)
    return text