import streamlit as st
import altair as alt

import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from src.database import SessionLocal

session = SessionLocal()

def fetch_all_multas():
    with SessionLocal() as session:
        result = session.execute("SELECT * FROM multas")  # Ajuste para a sua tabela
        return result.fetchall()

# Função para buscar multas filtradas por placa
def fetch_multas_by_placa(placa: str):
    with SessionLocal() as session:
        result = session.execute(
            "SELECT * FROM multas WHERE placa = :placa",
            {"placa": placa}
        )
        return result.fetchall()
