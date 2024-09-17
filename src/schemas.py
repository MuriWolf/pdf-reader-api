from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    senha: str
    nome_user: str
    username: str
    foto: str

class PdfContentBase(BaseModel):
    userId: int
    dataEnvio: int
    text: str

class TrafficViolationBase(BaseModel):
    id: int
    nome_pessoa: str
    placa_veiculo: str
    marca_veiculo: str
    especie: str
    infracao: str
    natureza: str
    pontuacao: str
    data_envio: int
    data_infracao: str
    hora_infracao: str
    endereco_infracao: str
    velocidade_regulamentada: str
    velocidade_media: str
    velocidade_considerada: str
    enquadramento: str
    artigo_ctb: str
    numero_ait: str
    data_limite_ind_condutor: str
    nro_infraest: str
    identificacao_equipamento: str
    afericao_certificacao: str
    agente_transito: str


