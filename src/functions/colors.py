import math
import re
import random

def get_random_num() -> int:
    return random.randint(52, 235)

def get_random_rgb() -> str:
    return f"rgb({get_random_num()}, {get_random_num()}, {get_random_num()})"

def convert_to_rgba(rgb_code: str, opacity: float) -> str:
    # Extraindo os valores RGB do código gerado
    rgb_values = rgb_code[rgb_code.find("(")+1:rgb_code.find(")")]
    return f"rgba({rgb_values}, {opacity})"

def convert_list_to_rgba(rgb_list: list[str], opacity: float) -> list[str]:
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


def convert_rgb_to_list(rgb: str) -> list:
    match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", rgb)
    if match:
        r, g, b = map(int, match.groups())
    
    return [r, g, b]

def convert_rgba_to_list(rgba: str) -> list:
    match = re.match(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)", rgba)
    if match:
        r, g, b, a = map(int, match.groups())
    
    return [r, g, b, a]

def diff_color(first_color: list[int], second_color: list[int]) -> int:
    sum_diff: int = 0
    for i in range(0, len(first_color)):
        sum_diff += abs(first_color[i] - second_color[i])
    return sum_diff 
    
def is_color_different_from_others(colors: list, new_color_str: str) -> bool:
    difference_needed = 150
    difference_needed -= 50 * math.floor(len(colors) / 10)

    if difference_needed < 15:
        difference_needed = 15 

    if len(colors) > 0:
        for color in colors:
            existing_color: list[int] = convert_rgb_to_list(color)
            new_color: list[int] = convert_rgb_to_list(new_color_str)

            if diff_color(new_color, existing_color) <= difference_needed:
                return False

    return True 

def lighten_color(color: str) -> str:
    color = convert_rgb_to_list(color)
    lighten_color = [0, 0, 0]

    for i in range(0, len(color)):
        lighten_color[i] = round(color[i] * 1.15)

    return f"rgb({lighten_color[0]}, {lighten_color[1]}, {lighten_color[2]})"

# TESTE DE FUNCIONAMENTO 

background_color = []
hover_background_color = []


#Logica para criar as paletas de cores para cada grafico
#Por exemplo: no grafico de natureza teria que ser range(0, 3 -> os três diferentes tipos de natureza de multa)


for i in range(0, 10): 
    color = get_random_rgb()
    while (not is_color_different_from_others(background_color, color)): # irá gerar outra cor caso não for diferente das demais já existentes
        color = get_random_rgb()

    background_color.append(color) 
    hover_background_color.append(lighten_color(color)) # adiciona a cor clereada nesta lista

print(background_color)
print(hover_background_color)