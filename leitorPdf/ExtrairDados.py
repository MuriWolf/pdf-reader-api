from pypdf import PdfReader
import re


def extrair_dados(texto_extraido, termos_chave):
    texto_formatado = texto_extraido
    # Inicializa um dicionário para armazenar os dados extraídos
    dados = {}
    
    # Define regex patterns para os termos chave e seus valores
    padroes = {
        "PLACA": r"PLACA\s+([^\n]+)",
        "MARCA": r"MARCA\s+([^\n]+)",
        "ESPÉCIE": r"ESPÉCIE\s+([^\n]+)",
        "NOME DO PROPRIETÁRIO": r"NOME DO PROPRIETÁRIO\s+([^\n]+)",
        "INFRAÇÃO": r"INFRAÇÃO\s+([^\n]+)",
        "LOCAL": r"LOCAL\s+([^\n]+)",
        "DATA DA INFRAÇÃO": r"DATA DA INFRAÇÃO\s+(\d{2}/\d{2}/\d{4})",
        "HORA": r"HORA\s+([^\n\d]+)",
        "VELOCIDADE REGULAMENTADA": r"VELOCIDADE REGULAMENTADA\s+KM/H(\d+)",
        "VELOCIDADE MEDIDA": r"VELOCIDADE MEDIDA\s+KM/H(\d+)",
        "VELOCIDADE CONSIDERADA": r"VELOCIDADE CONSIDERADA\s+KM/H(\d+)",
        "ENQUADRAMENTO": r"ENQUADRAMENTO\s+([^\n]+)",
        "ARTIGO DO CTB": r"ARTIGO DO CTB\s+([^\n]+)",
        "NATUREZA": r"NATUREZA\s+([^\n]+)",
        "PONTUAÇÃO": r"PONTUAÇÃO\s+([^\n]+)",
        "Nº AIT": r"Nº AIT\s+([^\n]+)",
        "DATA LIMITE IND. CONDUTOR / DEFESA AUTUAÇÃO": r"DATA LIMITE IND. CONDUTOR / DEFESA AUTUAÇÃO\s+([^\n]+)",
        "NRO. INFRAEST": r"NRO. INFRAEST\s+([^\n]+)",
        "IDENTIFICAÇÃO DO EQUIPAMENTO": r"IDENTIFICAÇÃO DO EQUIPAMENTO\s+([^\n]+)",
        "AFERIÇÃO / CERTIFICAÇÃO": r"AFERIÇÃO / CERTIFICAÇÃO\s+([^\n]+)",
        "AGENTE DE TRÂNSITO": r"AGENTE DE TRÂNSITO\s+(\d+)"
    }
    
    # Para cada padrão, encontra e armazena o valor correspondente no dicionário
    for termo_chave in termos_chave:
        nome_variavel = termo_chave["nome"]
        termo_pesquisar = termo_chave["pesquisar"]

        # Modificando o padrão para usar grupos nomeados
        padrao = rf"\b{re.escape(termo_pesquisar)}\s*([^\n]+)"

        match = re.search(padrao, texto_formatado)
        if match:
            # Verifica se a chave é 'agente_trânsito'
            if nome_variavel == 'agente_transito':
                # Extrai somente os dígitos após o termo "AGENTE DE TRÂNSITO"
                agente_transito = re.search(r'\b\d+\b', match.group(1))
                if agente_transito:
                    dados[nome_variavel] = agente_transito.group(0)
            elif 'velocidade' in nome_variavel.lower():
                # Extrai apenas os valores numéricos
                valor_numerico = re.search(r'\d+', match.group(1))
                if valor_numerico:
                  dados[nome_variavel] = valor_numerico.group(0)
            elif nome_variavel == 'hora_infracao':
                hora = re.search(r'[^\d]*(\d{2}:\d{2})', match.group(1))
                if hora:
                    dados[nome_variavel] = hora.group(1)
            else:
                dados[nome_variavel] = match.group(1).strip()

    return dados