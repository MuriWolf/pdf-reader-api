from pydantic import BaseModel, ConfigDict
from typing import Optional
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

class GraphicData(BaseModel):
    id: int
    marca_veiculo: Optional[str] = None  
    infracao: Optional[str] = None       
    natureza: Optional[str] = None        
    data_infracao: Optional[str] = None 
    endereco_infracao: Optional[str] = None 
    velocidade_regulamentada: Optional[str] = None  
    enquadramento: Optional[str] = None 
    background_color: Optional[str] = None
    hover_background_color: str = None

    class Config:
        exclude_none = True

class Dataset(BaseModel):
    label: str
    data: list[str]
    backgroundColor: list[str]
    hover_backgroundColor: list[str]

class GraphPie(BaseModel):
    label: str
    data: list[str]
    backgroundColor: list[str]
    hover_backgroundColor: list[str]

class GraphBar(BaseModel):
    label: str
    data: list[str]
    backgroundColor: list[str]
    borderWidth: int
    borderColor: list[str]

class GraphLine(BaseModel):
    label: list[str]
    fill: bool
    backgroundColor: str
    lineTension: float
    borderColor: str
    borderCapStyle: str
    borderDash: list
    borderDashOffset: float
    borderJoinStyle: str
    pointBorderColor: str
    pointBackgroundColor: str
    pointBorderWidth: int
    pointHoverRadius: int
    pointHoverBackgroundColor: str
    pointHoverBorderColor: str
    pointHoverBorderWidth: int
    pointRadius: int
    pointHitRadius: int
    data: list[str]

class ChartResponse(BaseModel):
    data_infracao: list[GraphLine] = None
    natureza: list[GraphPie] = None
    modelo_veiculo: list[GraphBar] = None
    velocidade_regulamentada: list[GraphPie] = None
    enquadramento: list[GraphBar] =  None
    endereco: list[Dataset] = None



class Color(BaseModel):
    background_color: str | None
    hover_background_color: str


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


