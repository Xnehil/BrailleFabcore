import cv2
import pytesseract
import textoABraille as tb
import numpy as np
import pymupdf
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe' #Cambiar por la ruta de tesseract en su computadora o comentar si ya esta en el PATH

def convertirImagen(imagen, debug=False):
    # Convertir imagen a escala de grises
    imagen = preprocesarImagen(imagen)
    #Sacar el texto de la imagen
    texto = pytesseract.image_to_string(imagen, lang='spa')
    # Texto a braille
    if debug:
        print("Texto conseguido de la imagen: ", texto)
    braille = tb.convertirTextoABraille(texto)
    return braille

def preprocesarImagen(imagen, resize_factor=4):
    norm_img = np.zeros((imagen.shape[0], imagen.shape[1]))
    imagen = cv2.normalize(imagen, norm_img, 0, 255, cv2.NORM_MINMAX)
    imagen = cv2.bitwise_not(imagen)

    imagen = cv2.resize(imagen, (imagen.shape[1] * resize_factor, imagen.shape[0] * resize_factor))
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # cv2.fastNlMeansDenoising(imagen, imagen, 10, 7, 21)
    #Esto en teoría ayuda al tesseract a reconocer mejor el texto escrito a mano
    kernel = np.ones((3,3),np.uint8)
    imagen = cv2.dilate(imagen, kernel, iterations=1)
    imagen = cv2.erode(imagen, kernel, iterations = 1)
    # imagen = cv2.medianBlur(imagen, 3)
    imagen = cv2.adaptiveThreshold(imagen,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
 cv2.THRESH_BINARY,11,2)
    return imagen

def process_png(file_path):
    image = cv2.imread(file_path)
    processed_image = preprocesarImagen(image)
    # Guardar imagen procesada para debug
    cv2.imwrite('processed_image.png', processed_image)
    text = pytesseract.image_to_string(processed_image, lang='spa')
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
            text += pytesseract.image_to_string(processed_image, lang='spa')
    return text