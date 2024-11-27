from datetime import datetime
from collections import defaultdict
import pandas as pd
import chardet
import os.path
import src.functions.colors as colors
from pathlib import Path
import src.constants as constants

file = "consultaInfracao.csv"
path = f"{Path(__file__).parent}/{file}"
norm_path = os.path.normpath(path=path)

with open(norm_path, "rb") as f:
    result = chardet.detect(f.read())
    print(result)


def contar_natureza(natureza_data: list[str]):
    natureza_dados = {
        "Leve": 0,
        "Media": 0,
        "Grave": 0,
        "Gravíssima": 0
    }


    for natureza in natureza_data:
        if natureza in natureza_dados:
            natureza_dados[natureza] += 1

    return natureza_dados

def criar_cor_natureza(natureza: list) -> list[str]:
    classificações = ["Leve", "Media", "Grave", "Gravíssima"]
    classificacao_cores = {}

    backgroundcolors = []
    hovercolors = []

    natureza_tipos = contar_natureza(natureza)

    for classificacao in classificações:
        if natureza_tipos[classificacao] >= 0:
            while True:
                color = colors.get_random_rgb()

                if color not in classificacao_cores.values():
                    classificacao_cores[classificacao] = color
                    break
    
    for classificacao, color in classificacao_cores.items():
        backgroundcolors.append(color)
        hovercolors.append(colors.lighten_color(color))

    
    return {
        "BackgroundColor": backgroundcolors,
        "HoverColor": hovercolors 
    }

def contar_marca(marca_veiculo_dados: list[str]):
    ocorrencias_color = {}
    backgroundcolor = []
    hovercolor = []

    ocorrencias = defaultdict(int)

    for marca in marca_veiculo_dados:
        ocorrencias[marca] += 1

        color = colors.get_random_rgb()
        if color not in ocorrencias_color.values():
            ocorrencias_color[marca] = color
    
    for marca, color in ocorrencias_color.items():
        backgroundcolor.append(color)
        hovercolor.append(colors.lighten_color(color))
    
    return{
        "label": ocorrencias.keys(),
        "data": ocorrencias.values(),
        "BackgroundColor": backgroundcolor,
        "HoverColor": hovercolor 
    }


def contar_data(data_infracao_dados: list[str]):


    datas = [datetime.strptime(data.strip(), "%d/%m/%Y") for data in data_infracao_dados]

    ano = [data.year for data in datas]
    ano_min = min(ano)
    ano_max = max(ano) 

    contador = defaultdict(int)
    for data in datas:
        if ano_min <= data.year <= ano_max:
            contador[data.year] += 1
    
    return contador


def str_to_int(velocidade_regulamentada: list[str]):
    lista_inteiros = []
    for item in velocidade_regulamentada:
        numero_string = item.replace(" km/h", "").replace(" ", "")
        if numero_string.isdigit():
            lista_inteiros.append(int(numero_string))
            



    return lista_inteiros

datas = ["28/04/2022", "11/08/2023", "14/06/2024"]
datas_ano = []
for data in datas:
    data_limpa = data.strip()
    datas_ano.append(datetime.strptime(data, "%d/%m/%Y"))


enquadramento_lista = ["74550", "55830", "74550"]

def contar_enquadramento(enquadramento_list: list):
    backgroundcolor = []
    hovercolor = []
    colors_dict = {}

    df = pd.read_csv(norm_path, sep=';', encoding='latin1')
    df.columns = df.columns.str.strip()  # Remove espaços extras
    df.columns = df.columns.str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8")
    #print(df.columns)

    # Normalizar os valores do CSV
    df['Codigo de infracao'] = df['Codigo de infracao'].astype(str).str.strip()
    df['Infracao'] = df['Infracao'].astype(str).str.strip()

    # Criar o dicionário de códigos para descrições
    codigos = dict(zip(df['Codigo de infracao'], df['Infracao']))

    # Normalizar a lista de entrada
    enquadramento_list = [str(codigo).strip() for codigo in enquadramento_list]

    contador = {}
    resultado = {}

    for codigo in enquadramento_list:
        contador[codigo] = contador.get(codigo, 0) + 1

        if contador[codigo] >= 0:
            color = colors.get_random_rgb()
            if color not in colors_dict.values():
              colors_dict[codigo] = color
    
    for codigo, color in colors_dict.items():
        backgroundcolor.append(color)
        hovercolor.append(colors.lighten_color(color))
    
    for codigo, ocorrencia in contador.items():
        descricao = codigos.get(codigo, "Descrição Não Encontrada")
        resultado[descricao] = ocorrencia
    
    return{
        "codigo": contador[codigo],
        "descricao": resultado[descricao],
        "backgroundcolor": backgroundcolor,
        "hovercolor": hovercolor,
        "data": resultado,
    } 

print(contar_enquadramento(enquadramento_list=enquadramento_lista))