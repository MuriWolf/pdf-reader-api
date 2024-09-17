import re
import src.functions.ExtrairDados as ExtrairDados 
def main(doc_texto):
    termos_chave = [
        {"nome": "nome_pessoa", "pesquisar": "NOME DO PROPRIETÁRIO"},
        {"nome": "placa_veiculo", "pesquisar": "PLACA"},
        {"nome": "marca_veiculo", "pesquisar": "MARCA"},
        {"nome": "especie", "pesquisar": "ESPÉCIE"},
        {"nome": "infracao", "pesquisar": "INFRAÇÃO"},
        {"nome": "endereco_infracao", "pesquisar": "LOCAL"},
        {"nome": "data_infracao", "pesquisar": "DATA DA INFRAÇÃO"},
        {"nome": "hora_infracao", "pesquisar": "HORA"},
        {"nome": "velocidade_regulamentada", "pesquisar": "VELOCIDADE REGULAMENTADA"},
        {"nome": "velocidade_media", "pesquisar": "VELOCIDADE MEDIDA"},
        {"nome": "velocidade_considerada", "pesquisar": "VELOCIDADE CONSIDERADA"},
        {"nome": "enquadramento", "pesquisar": "ENQUADRAMENTO"},
        {"nome": "artigo_ctb", "pesquisar": "ARTIGO DO CTB"},
        {"nome": "natureza", "pesquisar": "NATUREZA"},
        {"nome": "pontuacao", "pesquisar": "PONTUAÇÃO"},
        {"nome": "numero_ait", "pesquisar": "Nº AIT"},
        {"nome": "data_limite_ind_condutor", "pesquisar": "DATA LIMITE IND. CONDUTOR / DEFESA AUTUAÇÃO"},
        {"nome": "nro_infraest", "pesquisar": "NRO. INFRAEST"},
        {"nome": "identificacao_equipamento", "pesquisar": "IDENTIFICAÇÃO DO EQUIPAMENTO"},
        {"nome": "afericao_certificacao", "pesquisar": "AFERIÇÃO / CERTIFICAÇÃO"},
        {"nome": "agente_transito", "pesquisar": "AGENTE DE TRÂNSITO"}
    ]

    texto = doc_texto

    def adicionar_espacos_apos_termos(texto):
        for termo_chave in termos_chave:
            termo_pesquisar = termo_chave["pesquisar"]
            texto = re.sub(r'(\S)(' + re.escape(termo_pesquisar) + r')(\S)', r'\1 \2 \3', texto)
            texto = re.sub(r'(\S)(' + re.escape(termo_pesquisar) + r')', r'\1 \2', texto)
            texto = re.sub(r'(' + re.escape(termo_pesquisar) + r')(\S)', r'\1 \2', texto)
        texto = re.sub(r'([a-z])([A-Z0-9])', r'\1 \2', texto)
        texto = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', texto)
        texto = re.sub(r'([0-9])([A-Z])', r'\1 \2', texto)
        texto = re.sub(r'(\.)([A-Z])', r'\1 \2', texto)
        texto = re.sub(r'(,)([A-Z])', r'\1 \2', texto)
        texto = re.sub(r'(\w+-SP)(COD)', r'\1 \2', texto)
        return texto

    def quebra_linha(texto):
        for termo in termos_chave:
            termo_pesquisar = termo["pesquisar"]
            if termo != "DATA DA INFRAÇÃO":
                texto = re.sub(r'(\b' + re.escape(termo_pesquisar) + r'\b)', r'\n\1', texto)
        texto = re.sub(r"DATA DA\s*\nINFRAÇÃO", "DATA DA INFRAÇÃO", texto)
        texto = re.sub(r"([A-Z][A-Z]+-[A-Z][A-Z]+) (COD\. LOC\. EQUIP\.)", r"\1\n\2", texto)
        return texto
    
    
    texto_espaço = adicionar_espacos_apos_termos(texto)
    texto_formatado = quebra_linha(texto_espaço)
    texto_formatado = re.sub(r"(COD\. LOC\. EQUIP\.\d{4})( DATA DA INFRAÇÃO)", r"\1\n\2", texto_formatado)

    dados_extraidos = ExtrairDados.extrair_dados(texto_formatado, termos_chave)

    for chave, valor in dados_extraidos.items():
    # Imprimir cada chave e seu valor correspondente
     print(f"{chave}: {valor}")

    return dados_extraidos

if __name__ == "__main__":
    main()
