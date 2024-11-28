from collections import defaultdict
import src.fines.graphs.colors as colors

def retornar_dados_velocidade_regulamentada(velocidade_dados: list):
    ocorrencias = defaultdict(int)
    backgroundcolor = []
    hovercolor = []
    color_dict = {}

    for velocidade in velocidade_dados:
        ocorrencias[velocidade] += 1

        if ocorrencias[velocidade] > 0:
            color = colors.retornar_rgb_aleatorio()
            if color not in color_dict:
                color_dict[velocidade] = color
    
    for velocidade, color in color_dict.items():
        backgroundcolor.append(color)
        hovercolor.append(colors.clarear_cor(color))
    
    return {
        "label": [ocorrencia+"km" for ocorrencia in ocorrencias.keys()],
        "Data": ocorrencias.values(),
        "backgroundcolor": backgroundcolor,
        "hovercolor": hovercolor
    }