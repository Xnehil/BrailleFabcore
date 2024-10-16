import cv2
import pytesseract
import textoABraille as tb

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

def preprocesarImagen(imagen):
    # Aplicar filtro de mediana
    # imagen = cv2.medianBlur(imagen, 5)
    return imagen