import pandas as pd
import plotly.express as px
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.database import SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import text
from src.settings import Settings

settings = Settings()


# Função para buscar todas as multas
def fetch_all_multas():
    with SessionLocal() as session:
        result = session.execute(text('SELECT * FROM pdf'))  # Ajuste para a sua tabela e campos
        data = result.fetchall()
        
        # Convertendo os dados para um DataFrame do Pandas
        df = pd.DataFrame(data, columns=["nome_pessoa", "pontuacao"])
        return df

dataframe = fetch_all_multas()

print(dataframe)

fig = px.pie(dataframe, 
             names="nome_pessoa", 
             values="pontuacao", 
             title="Distribuição de Pontuação por Pessoa")

fig.show()

# Exportando para JSON
dataframe.to_json('dados_grafico.json', orient='records')
