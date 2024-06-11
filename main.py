from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Annotated
import sql_app.models as models
from sql_app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from leitorPdf import LeitorFinal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PdfContentBase(BaseModel):
    userId: int
    dataEnvio: int
    text: str

class UserBase(BaseModel):
    email: str
    senha: str
    nome_user: str
    username: str
    foto: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def search_user(list, search_value):
    for i in list:
        if i == "":
            return i
    return None 


class Fine_content(BaseModel):
    lastModified: int
    text: str

class Traffic_violation(BaseModel):
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


class User(BaseModel):
    id: int
    email: str
    senha: str
    nome_user: str
    username: str
    foto: str

users: List[User] = [
    { 
        "email": "lobao@gmail.com",
        "senha": "12345678",
        "nome_user": "Hermann Hesse",
        "username": "HermannHesse",
        "foto": "asdasdas"
    },
    { 
        "email": "erikaodms@gmail.com",
        "senha": "12345678",
        "nome_user": "Erik Satie",
        "username": "ErikSatie",
        "foto": "asdasdas"
    },
    { 
        "email": "sorime@gmail.com",
        "senha": "12345678",
        "nome_user": "Gustave Dore",
        "username": "GustaveDore",
        "foto": "asdasdas"
    }
]

@app.post("/fines", status_code=status.HTTP_201_CREATED)
async def post_fine_data(fines_data: List[PdfContentBase], db: db_dependency):
    for fine in fines_data: 
        fine_values = LeitorFinal.main(fine.text)
        # return fine_values
        db_fine = models.PDF(**fine_values, user_id=fine.userId, 
        data_envio=fine.dataEnvio)
        db.add(db_fine)
        db.commit()
        db.refresh(db_fine)
    return { "code": 200, "msg": "success" }

@app.get("/fines", status_code=status.HTTP_200_OK)
async def get_fines(db: db_dependency, id_user: int | None = None, username: str = None):
    fines = []
    if (id_user):
        fines = db.query(models.PDF).filter(models.PDF.user_id == id_user).all()
    elif (username):
        user = db.query(models.User).filter(models.User.username == username).first()
        if (user):
            fines = db.query(models.PDF).filter(models.PDF.user_id == user.id_user).all()
        else:
            raise HTTPException(status_code=404, detail='Usuario não encontrado')
    else:
        fines = db.query(models.PDF).all()

    if (len(fines) == 0):
        raise HTTPException(status_code=404, detail='Nenhum documento foi encontrado')
    return fines

@app.get("/users", status_code=status.HTTP_200_OK)      
async def get_user(db: db_dependency, user_id: int = None, username: str = None):
    user = None
    if (user_id):
        user = db.query(models.User).filter(models.User.id_user == user_id).first()
    elif (username):
        user = db.query(models.User).filter(models.User.username == username).first()
    else:
        user = db.query(models.User).all()
    
    if user is None:
        raise HTTPException(status_code=404, detail='Usuario não encontrado')
    
    return user
        

# @app.get("/fines/{fine_id}")
# async def get_fine(fine_id: int):
#     # do logic to communicate with the backend
#     return fine

# @app.post("/users/", status_code=status.HTTP_201_CREATED)
# async def create_user(user: UserBase, db: db_dependency):
#     db_user = models.User(**user.model_dump())
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user