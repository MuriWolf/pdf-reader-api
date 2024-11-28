from collections import defaultdict
import src.fines.graphs.colors as colors

def retornar_dados_marca(marca_veiculo_dados: list[str]):
    ocorrencias_color = {}
    backgroundcolor = []
    hovercolor = []

    ocorrencias = defaultdict(int)

    for marca in marca_veiculo_dados:
        ocorrencias[marca] += 1

        color = colors.retornar_rgb_aleatorio()
        if color not in ocorrencias_color.values():
            ocorrencias_color[marca] = color
    
    for marca, color in ocorrencias_color.items():
        backgroundcolor.append(color)
        hovercolor.append(colors.clarear_cor(color))
    
    return{
        "label": ocorrencias.keys(),
        "data": ocorrencias.values(),
        "BackgroundColor": backgroundcolor,
        "HoverColor": hovercolor 
    }