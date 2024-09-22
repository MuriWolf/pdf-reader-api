from pydantic import BaseModel, ConfigDict
import src.models as models

class MessageResponse(BaseModel):
    code: int
    msg: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None

class UserLogin(BaseModel):
    email: str
    senha: str

class UserBase(BaseModel):
    email: str
    senha: str
    nome_user: str
    role: str
    username: str 
    foto: str 

class UserUpdate(BaseModel):
    email: str | None = None
    senha: str | None = None
    nome_user: str | None = None
    username: str | None = None
    role: str | None = None
    foto: str | None = None

class UserPublic(BaseModel):
    id: int
    email: str
    nome_user: str
    username: str
    role: str 
    foto: str
    model_config = ConfigDict(from_attributes=True)

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


