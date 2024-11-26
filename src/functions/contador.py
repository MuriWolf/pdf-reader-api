from datetime import datetime
from collections import defaultdict
import pandas as pd
import chardet
import os.path
from pathlib import Path

file = "consultaInfracao.csv"
path = f"{Path(__file__).parent}/{file}"
norm_path = os.path.normpath(path=path)

with open(norm_path, "rb") as f:
    result = chardet.detect(f.read())
    print(result)


def contador_natureza(natureza_data: list[str]):
    leve = 0
    grave = 0
    gravissima = 0
    natureza_dados = []
    for natureza in natureza_data:
        if(natureza == "Leve"):
            leve += 1
            natureza_dados.append(leve)
        if(natureza == "Grave"):
            grave += 1
            natureza_dados.append(grave)
        if(natureza == "Gravíssima"):
            gravissima += 1
            natureza_dados.append(gravissima)
    return natureza_dados

def contador_data(data_infracao_dados: list[str]):


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

enquadramento_lista = ['74550', '54871', '74550', '12345', '74710']


def contador_enquadramento(enquadramento_list: list):
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

    for codigo in enquadramento_lista:
        
        contador[codigo] = contador.get(codigo, 0) + 1
    
    for codigo, ocorrencia in contador.items():
        descricao = codigos.get(codigo, "Descrição Não Encontrada")
        resultado[descricao] = ocorrencia
    
    return resultado

print(contador_enquadramento(enquadramento_list=enquadramento_lista))