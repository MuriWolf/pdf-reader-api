from collections import defaultdict
from src.fines.utils import utils
from datetime import datetime

def retornar_dados_data_da_infracao(data_infracao_dados: list[str]):
    '''
    Data nesse caso se refere ao tempo (PT: data = EN: date), não dado (PT: dado = EN: data).
    '''
    
    datas = [datetime.strptime(data.strip(), "%d/%m/%Y") for data in data_infracao_dados]

    anos = [data.year for data in datas]
    ano_min = min(anos)
    ano_max = max(anos) 

    anos_intervalo = utils.criar_intervalo_de_inteiro(ano_min, ano_max)
    anos_str_intervalo = [str(ano) for ano in anos_intervalo] 
    
    contador = defaultdict(int)
    for data in datas:
        contador[data.year] += 1

    return {
        "data": list(contador.values()),
        "anos": anos_str_intervalo
    }