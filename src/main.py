from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Annotated
import src.models as models
from src.database import engine, SessionLocal
from sqlalchemy.orm import Session
from src.fines.readers import reader
from src.fines.graphs import colors, create_data
from src.schemas import UserBase, UserPublic, UserUpdate, PdfContentBase, Token, UserLogin, MessageResponse, ChartResponse, GraphLine, GraphBar, GraphPie, GraphPieDataset, GraphLineDataset, GraphBarDataset
from src.security import get_password_hash, verify_password, create_token, get_current_user, validate_refresh_token
from src.utils import convert_user_to_public, is_update_from_commom_user_valid
from datetime import timedelta
from src.settings import Settings
import logging
from src.fines.graphs.constants import CORES_NATUREZAS_MULTA
from src.fines.graphs.create_data import retornar_dados_enquadramento, retornar_dados_data_da_infracao, retornar_dados_marca, retornar_dados_natureza, retornar_dados_velocidade_regulamentada 

settings = Settings()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

@app.post("/fines", status_code=status.HTTP_201_CREATED)
async def post_fine_data(fines_data: List[PdfContentBase], db: db_dependency):
    for fine in fines_data: 
        fine_values = reader.main(fine.text)
        # return fine_values
        db_fine = models.PDF(**fine_values, user_id=fine.userId, data_envio=fine.dataEnvio)
        db.add(db_fine)
        db.commit()
        db.refresh(db_fine)
    return { "code": 200, "msg": "success" }

@app.get("/fines", status_code=status.HTTP_200_OK)
async def get_fines(db: db_dependency, id_user: int | None = None, username: str | None = None):
    fines = []
    if (id_user):
        fines = db.query(models.PDF).filter(models.PDF.user_id == id_user).all()
    elif (username):
        user = db.query(models.User).filter(models.User.username == username).first()
        if (user):
            fines = db.query(models.PDF).filter(models.PDF.user_id == user.id_user).all()
        else:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado.')
    else:
        fines = db.query(models.PDF).all()

    if (len(fines) == 0):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Nenhum documento foi encontrado.')
    return fines

@app.post("/users", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, user: UserBase):
    db_user = db.query(models.User).filter(models.User.username == user.username or models.User.email == user.email).first()

    if (db_user):
        if (db_user.username == user.username):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username já existe.'
            )
        elif (db_user.email == user.email):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email já existe.'
            )
        
    hashed_password = get_password_hash(user.senha)
    db_user = models.User(
        username=user.username,
        email=user.email,
        nome_user=user.nome_user,
        senha=hashed_password, 
        role=user.role,
        foto=''
    )

    db.add(db_user)    
    db.commit()
    db.refresh(db_user)

    response_user = convert_user_to_public(db_user)
    return response_user

@app.get("/users", status_code=status.HTTP_200_OK)      
async def get_user(db: db_dependency, user_id: int | None = None, username: str | None = None, email: str | None = None):
    user = None
    users = None
    if (user_id):
        user = db.query(models.User).filter(models.User.id_user == user_id).first()
    elif (email):
        user = db.query(models.User).filter(models.User.email == email).first()
    elif (username):
        user = db.query(models.User).filter(models.User.username == username).first()
    else:
        users = db.query(models.User).all()
        users = [convert_user_to_public(u) for u in users]
    
    if user is None and users is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado.')
    elif user is None:
        return users
    else:
        return convert_user_to_public(user)


@app.get("/graph", status_code=status.HTTP_200_OK, response_model=ChartResponse)
async def create_data(
    db: db_dependency, 
    id_user: int | None = None, 
    username: str | None = None
):
    fines = await get_fines(db, id_user, username)

    if not fines:
        raise HTTPException(status_code=404, detail="Nenhuma multa encontrada.")

    background_colors = []
    hover_background_colors = []

    data_infracao_data = []
    natureza_data = []
    marca_veiculo_data = []
    velocidade_regulamentada_data = []
    enquadramento_data = []
    endereco_data = []

    anos = ["2021","2022", "2023", "2024"]

    color1 = colors.retornar_rgb_aleatorio()
        
    #Contador de Ocorrencias
    
    for fine in fines:
        data_infracao_data.append(fine.data_infracao)
        natureza_data.append(fine.natureza)
        marca_veiculo_data.append(fine.marca_veiculo)
        velocidade_regulamentada_data.append(fine.velocidade_regulamentada)
        enquadramento_data.append(fine.enquadramento)
        endereco_data.append(fine.endereco_infracao)

        color = colors.retornar_rgb_aleatorio()
        while not colors.verificar_cor_diferente_das_existentes(background_colors, color):
            color = colors.retornar_rgb_aleatorio()

        background_colors.append(color)
        hover_background_colors.append(colors.clarear_cor(color))

    #Funções para contagem de ocorrencias de determinados dados com suas respecitvos rotulos(labels)
    natureza_dict = retornar_dados_natureza(natureza_data)
    velocidade_dict = retornar_dados_velocidade_regulamentada(velocidade_regulamentada_data)
    data_dict = retornar_dados_data_da_infracao(data_infracao_data)
    marca_dict = retornar_dados_marca(marca_veiculo_data)
    enquadramento_dict = retornar_dados_enquadramento(enquadramento_data)

    #Grafico de Linhas
    data_infracao_graph = GraphLine(
            labels = data_dict['anos'],
            datasets = [
                GraphLineDataset(
                    label = "Grafico de Data da Infração (Por Ano)",
                    fill = True,
                    backgroundColor = colors.converter_para_rgba(color1, 0.3),
                    lineTension = 0.3,
                    borderColor = colors.clarear_cor(color),
                    borderCapStyle = 'butt',
                    borderDash = [],
                    borderDashOffset =  0.0,
                    borderJoinStyle =  'miter',
                    pointBorderColor = '205, 130,1 58',
                    pointBackgroundColor = '255, 255, 255',
                    pointBorderWidth = 10,
                    pointHoverRadius = 5,
                    pointHoverBackgroundColor = '0, 0, 0',
                    pointHoverBorderColor =  '220, 220, 220,1',
                    pointHoverBorderWidth =  2,
                    pointRadius =  1,
                    pointHitRadius = 10,
                    data = data_dict['data']
                )]
        )

    #Grafico de Barra
    enquadramento_graph = GraphBar(
            labels = enquadramento_dict['codigo'],
            datasets=[
                GraphBarDataset(
                    label= enquadramento_dict['descricao'],
                    data = list(enquadramento_dict['data']),
                    backgroundColor=colors.converter_lista_para_rgba(enquadramento_dict['backgroundcolor'], 0.4),
                    borderWidth=2,
                    borderColor=colors.converter_lista_para_rgba(enquadramento_dict['hovercolor'], 1.0)
                )
            ]
       )

    marca_graph = GraphBar(
        labels = marca_dict["label"],
        datasets=[
            GraphBarDataset(
                label=marca_dict['label'],
                data=marca_dict['data'],
                backgroundColor = colors.converter_lista_para_rgba(marca_dict['BackgroundColor'], 0.4),
                borderWidth= 2,
                borderColor=colors.converter_lista_para_rgba(marca_dict['HoverColor'], 1.0)
            )
        ]
    )

    #Grafico Pie ou Doughnut
    natureza_graph = GraphPie(
        labels = ["Leve", "Media", "Grave", "Gravíssima"],
        datasets=[
            GraphPieDataset(
                label = "Grafico de Natureza da Infração",
                data=natureza_dict.values(),
                backgroundColor=CORES_NATUREZAS_MULTA["backgroundColor"],
                hover_backgroundColor=CORES_NATUREZAS_MULTA["hover_backgroundColor"]
            )
        ]
    )
    
    velocidade_regulamentada_graph= GraphPie(
        labels = velocidade_dict['label'],
        datasets=[
            GraphPieDataset(
               label = "Grafico de Velocidade Regulamentada",
               data=velocidade_dict['Data'],
               backgroundColor= velocidade_dict['backgroundcolor'],
               hover_backgroundColor=velocidade_dict['hovercolor']
            )
        ]
    )

    return ChartResponse(data_infracao=data_infracao_graph,  natureza=natureza_graph, velocidade_regulamentada= velocidade_regulamentada_graph,  enquadramento=enquadramento_graph, marca_veiculo=marca_graph)

@app.get("/users/me", response_model=UserPublic, status_code=status.HTTP_200_OK)
def read_users_me(
        db: db_dependency,
        current_user: models.User = Depends(get_current_user)
    ):
    return convert_user_to_public(current_user)

@app.patch('/users/{user_id}', response_model=UserPublic, status_code=status.HTTP_200_OK) 
def update_user(
    db: db_dependency,
    user_id: int,
    user: UserUpdate,
    current_user: models.User = Depends(get_current_user)
):
    user_valid_update = is_update_from_commom_user_valid(user=user, attrs_allowed=["foto"]) 

    if (current_user.role.value != "admin"):
        if (current_user.id_user != user_id or not user_valid_update):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='Sem permissões suficientes'
            )

    db_user = db.query(models.User).filter(models.User.id_user == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado'
        )

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    response_user = convert_user_to_public(db_user)

    return response_user 

@app.delete("/users/{user_id}", response_model=MessageResponse)
def delete_user(
    db: db_dependency,
    user_id: int,
    current_user: models.User = Depends(get_current_user)
):
    if (current_user.role.value != "admin"):
        if (current_user.id_user != user_id):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='Sem permissões suficientes'
            )

    db_user = db.query(models.User).filter(models.User.id_user == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuario não encontrado" 
        )

    db.delete(db_user)
    db.commit()

    return {'code': HTTPStatus.OK, 'msg': 'Usuario deletado'}

@app.post("/token", response_model=Token)
def login_for_access_token(
    db: db_dependency,
    form_data: UserLogin
):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email ou usuario incorreto"
        )
    
    if not verify_password(form_data.senha, user.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email ou usuario incorreto"
        ) 
    
    access_token = create_token(data={ 'sub': user.email, 'role': user.role.value }, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token(data={ 'sub': user.email, 'role': user.role.value }, expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}

@app.post("logout")
async def logout(token: Token):
    # revoked_tokens.add(token)
    return { "code": 200, "message": "Deslogado com sucesso" }

@app.post("/refresh", response_model=Token)
def refresh_access_token(
    token_data: Annotated[tuple[models.User, str], Depends(validate_refresh_token)]
):
    user, refresh_token = token_data
    new_access_token = create_token(data={'sub': user.email, 'role': user.role.value}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    return {'access_token': new_access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}