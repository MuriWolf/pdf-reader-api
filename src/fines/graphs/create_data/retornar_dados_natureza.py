import src.fines.graphs.constants as constants

def retornar_dados_natureza(naturezas_data: list[str]):
    contagem_naturezas = {
        "LEVE": 0,
        "MEDIA": 0,
        "GRAVE": 0,
        "GRAVÍSSIMA": 0
    }

    for data in naturezas_data:
        if data.upper() in constants.CLASSIFICACOES_NATUREZAS_MULTA:
            contagem_naturezas[data.upper()] += 1

    return contagem_naturezas 