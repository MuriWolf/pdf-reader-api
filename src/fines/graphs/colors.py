import math
import re
import random

def retornar_inteiro_aleatorio() -> int:
    return random.randint(52, 235)

def retornar_rgb_aleatorio() -> str:
    return f"rgb({retornar_inteiro_aleatorio()}, {retornar_inteiro_aleatorio()}, {retornar_inteiro_aleatorio()})"

def converter_para_rgba(rgb_code: str, opacity: float) -> str:
    # Extraindo os valores RGB do código gerado
    rgb_values = rgb_code[rgb_code.find("(")+1:rgb_code.find(")")]
    return f"rgba({rgb_values}, {opacity})"

def converter_lista_para_rgba(rgb_list: list[str], opacity: float) -> list[str]:
    """
    Converte uma lista de cores RGB para RGBA com a opacidade especificada.
    
    Args:
        rgb_list (list[str]): Lista de strings no formato "rgb(R, G, B)".
        opacity (float): Valor da opacidade (0 a 1).
    
    Returns:
        list[str]: Lista de cores no formato "rgba(R, G, B, A)".
    """
    rgba_list = []
    for rgb_code in rgb_list:
        # Extraindo os valores RGB do código gerado
        rgb_values = rgb_code[rgb_code.find("(")+1:rgb_code.find(")")]
        rgba_list.append(f"rgba({rgb_values}, {opacity})")
    return rgba_list


def converter_rgb_para_lista(rgb: str) -> list:
    match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", rgb)
    if match:
        r, g, b = map(int, match.groups())
    
    return [r, g, b]

def converter_rgba_para_lista(rgba: str) -> list:
    match = re.match(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)", rgba)
    if match:
        r, g, b, a = map(int, match.groups())
    
    return [r, g, b, a]

def subtrair_colores(first_color: list[int], second_color: list[int]) -> int:
    sum_diff: int = 0
    for i in range(0, len(first_color)):
        sum_diff += abs(first_color[i] - second_color[i])
    return sum_diff 
    
def verificar_cor_diferente_das_existentes(colors: list, new_color_str: str) -> bool:
    difference_needed = 150
    difference_needed -= 50 * math.floor(len(colors) / 10)

    if difference_needed < 15:
        difference_needed = 15 

    if len(colors) > 0:
        for color in colors:
            existing_color: list[int] = converter_rgb_para_lista(color)
            new_color: list[int] = converter_rgb_para_lista(new_color_str)

            if subtrair_colores(new_color, existing_color) <= difference_needed:
                return False

    return True 

def clarear_cor(color: str) -> str:
    color = converter_rgb_para_lista(color)
    clarear_cor = [0, 0, 0]

    for i in range(0, len(color)):
        clarear_cor[i] = round(color[i] * 1.15)

    return f"rgb({clarear_cor[0]}, {clarear_cor[1]}, {clarear_cor[2]})"


