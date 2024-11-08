# Basado en este repo https://github.com/jungby/Braillenius?tab=readme-ov-file#future-changes-in-mind por jungby
braille_text_dict = {
    'á': '⠷', 'é': '⠮', 'í': '⠌', 'ó': '⠬', 'ú': '⠾', 'ü': '⠳', '\n': '\n', '...': ' ',
    ' ': ' ', '!': '⠖', '¡': '⠖', "'": '⠦', '#': '⠼', '$': '⠸⠎', '%': '⠸⠴', '&': '⠠⠯', '"': '⠦',
    '(': '⠣', ')': '⠜', '*': '⠔', ',': '⠂', '-': '⠤', '.': '⠄', '/': '⠠⠂', '0': '⠼⠚', '1': '⠼⠁',
    '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠲', '5': '⠼⠑', '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊',
    ':': '⠱', ';': '⠰', '<': '⠣', '=': '⠿', '>': '⠜', '?': '⠢', '¿': '⠢', '@': '⠈', 'a': '⠁', 'b': '⠃',
    'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇',
    'm': '⠍', 'n': '⠝', 'ñ': '⠻', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 'u': '⠥',
    'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵', '[': '⠣', ']': '⠜', '^': '⠘', '_': '⠸'
}

braille_signal_dict = {
    # Los puntos alzados serían 1 y los bajos 0. Estoy contando que el punto 1 de braille sería el el bit de más a la izquierda
    # Por ejemplo, la letra 'á': ⠷ en braille sería:
    #               0b   1  1  1  0  1  1
    #        N°Braille:  1  2  3  4  5  6
    ' ': 0b000000,  
    '⠁': 0b100000,  '⠂': 0b010000, '⠄': 0b001000,'⠈': 0b000100,'⠐': 0b000010,'⠠': 0b000001,  
    '⠃': 0b110000,  '⠅': 0b101000, '⠉': 0b100100,'⠑': 0b100010,'⠡': 0b100001,'⠆': 0b011000,  
    '⠊': 0b010100,  '⠒': 0b010010, '⠢': 0b010001,'⠌': 0b001100,'⠔': 0b001010,'⠤': 0b001001,  
    '⠘': 0b000110,  '⠨': 0b000101, '⠰': 0b000011,'⠇': 0b111000,'⠋': 0b110100,'⠓': 0b110010,  
    '⠣': 0b110001,  '⠍': 0b101100, '⠕': 0b101010,'⠥': 0b101001,'⠙': 0b100110,'⠩': 0b100101,  
    '⠱': 0b100011,  '⠖': 0b011010, '⠦': 0b011001,'⠚': 0b010110,'⠪': 0b010101,'⠲': 0b010011,  
    '⠜': 0b001110,  '⠬': 0b001101, '⠴': 0b001011,'⠸': 0b000111,'⠏': 0b111100,'⠗': 0b111010,  
    '⠧': 0b111001,  '⠝': 0b101110, '⠭': 0b101101,'⠵': 0b101011,'⠹': 0b100111,'⠛': 0b110110,  
    '⠫': 0b110101,  '⠳': 0b110011, '⠯': 0b111101,'⠽': 0b101111,'⠻': 0b110111,'⠷': 0b111011,  
    '⠟': 0b111110,  '⠮': 0b011101, '⠾': 0b011111,'⠼': 0b001111,'⠿': 0b111111, '⠚': 0b010110, 
    '⠪': 0b010101, '⠲': 0b010011, '⠜': 0b001110, '⠬': 0b001101, '⠴': 0b001011, '⠞': 0b011110,
    '⠎': 0b011100
}

braille_angle_dict = {
    # El servo solo puede moverse 180 y tenemos 8 posiciones posibles (0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5)
    0b000: 0, 0b001: 22.5, 0b010: 45, 0b011: 67.5, 0b100: 90, 0b101: 112.5, 0b110: 135, 0b111: 157.5 , ' ': 0
}

def convertirTextoABraille(cadena):
    braille = ""
    lower = cadena.strip().lower()
    for letra in lower:
        braille += braille_text_dict.get(letra, letra)
    return braille

def convertirASeñales(cadena):
    señales = []
    lower = cadena.strip().lower()
    for letra in lower:
        señales.append(braille_signal_dict.get(braille_text_dict.get(letra, letra), letra))
    return señales

def convertirAAngulos(cadena):
    angulos = []
    lower = cadena.strip().lower()
    for letra in lower:
        señal = braille_signal_dict.get(braille_text_dict.get(letra, letra), letra)
        # print(f'{letra}: {(señal)}')
        primerosTres = señal >> 3
        segundosTres = señal & 0b000111
        # Second angle represents the second Braille column (bits 4, 5, 6)
        angle1 = braille_angle_dict.get(primerosTres, 0)
        angle2 = braille_angle_dict.get(segundosTres, 0)
        angulos.append([angle1, angle2])
    return angulos