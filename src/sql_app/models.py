from sqlalchemy import String, Column, ForeignKey, Integer, Date, BigInteger
from sqlalchemy.orm import relationship

from .database import Base

class PDF(Base):
    __tablename__ = 'pdf'
    id_pdf = Column(Integer, primary_key=True)
    nome_pessoa = Column(String(30), nullable=False)
    placa_veiculo = Column(String(20), nullable=False)
    marca_veiculo = Column(String(20), nullable=False)
    especie = Column(String(40), nullable=False)
    infracao = Column(String(200), nullable=False)
    natureza = Column(String(20), nullable=False)
    pontuacao = Column(String(20), nullable=False)
    data_infracao = Column(String(20), nullable=False)
    hora_infracao = Column(String(300), nullable=False) # 30
    endereco_infracao = Column(String(200), nullable=False)
    velocidade_regulamentada = Column(String(20), nullable=False)
    velocidade_media = Column(String(20), nullable=False)
    velocidade_considerada = Column(String(20), nullable=False)
    enquadramento = Column(String(20), nullable=False)
    artigo_ctb = Column(String(20), nullable=False)
    numero_ait = Column(String(15), nullable=False)
    data_limite_ind_condutor = Column(String(20), nullable=False)
    nro_infraest = Column(String(20), nullable=False)
    identificacao_equipamento = Column(String(30), nullable=False)
    afericao_certificacao = Column(String(20), nullable=False)
    agente_transito = Column(String(100), nullable=False)
    data_envio = Column(BigInteger, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id_user"))

    user = relationship("User", back_populates="userData")

class User(Base):
    __tablename__ = "users" # mudar

    id_user = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    senha = Column(String(255))
    nome_user = Column(String(30))
    username = Column(String(30), unique=True)
    foto = Column(String(200))

    userData = relationship("PDF", back_populates="user")
