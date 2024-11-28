from pathlib import Path
import chardet
import os.path
import src.fines.graphs.colors as colors
import pandas as pd

file = "consultaInfracao.csv"
path = f"{Path(__file__).parent.parent.parent}/assets/{file}"
norm_path = os.path.normpath(path=path)

with open(norm_path, "rb") as f:
    result = chardet.detect(f.read())
    print(result)

def retornar_dados_enquadramento(enquadramentos_data: list):
    backgroundcolor = []
    hovercolor = []
    colors_dict = {}

    df = pd.read_csv(norm_path, sep=';', encoding='latin1')
    df.columns = df.columns.str.strip()  # Remove espaços extras
    df.columns = df.columns.str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8")

    # Normalizar os valores do CSV
    df['Codigo de infracao'] = df['Codigo de infracao'].astype(str).str.strip()
    df['Infracao'] = df['Infracao'].astype(str).str.strip()

    # Criar o dicionário de códigos para descrições
    codigos = dict(zip(df['Codigo de infracao'], df['Infracao']))

    # Normalizar a lista de entrada
    enquadramentos_data = [str(codigo).strip() for codigo in enquadramentos_data]

    contador = {}
    resultado = {}

    for codigo in enquadramentos_data:
        contador[codigo] = contador.get(codigo, 0) + 1

        if contador[codigo] >= 0:
            color = colors.retornar_rgb_aleatorio()
            if color not in colors_dict.values():
              colors_dict[codigo] = color
    
    for codigo, color in colors_dict.items():
        backgroundcolor.append(color)
        hovercolor.append(colors.clarear_cor(color))
    
    for codigo, ocorrencia in contador.items():
        descricao = codigos.get(codigo, "Descrição Não Encontrada")
        resultado[codigo] =  {"descricao": descricao, "ocorrencias": ocorrencia}

    return{
        "codigo": resultado.keys(),
        "descricao":  [item["descricao"] for item in resultado.values()],
        "backgroundcolor": backgroundcolor,
        "hovercolor": hovercolor,
        "data": [item["ocorrencias"] for item in resultado.values()],
    } 
