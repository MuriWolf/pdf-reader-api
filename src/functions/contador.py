from datetime import datetime
from collections import defaultdict

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
    print(datas_ano)